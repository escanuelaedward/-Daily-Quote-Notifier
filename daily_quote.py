# Main script to display a daily quote
# This script also logs the quotes shown to a file
# Will be able to install itself as a daily scheduled task on Windows

import argparse # For command line argument parsing
import csv # For reading quotes from a CSV file
import json # For reading configuration files
import os # For operating system related functions
import random # For selecting random quotes
import subprocess # For installing scheduled tasks
import sys # For system specific parameters and functions
from datetime import datetime # For handling date and time
from pathlib import Path # For handling file paths

from notify import notify # Importing the notification function from notify.py

# Paths and basic configurations

APP_NAME = "DailyQuoteNotifier"    # Application name
TITLE = "Daily Quote"              # Notification title

# ROOT is where the script is located
ROOT = Path(__file__).parent

# quotes.json lives in the same directory as the script
QUOTES_PATH = ROOT / "quotes.json"

# logs/ folder inside the project
LOGS_DIR = ROOT / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True) # Create logs directory if it doesn't exist
LOG_FILE = LOGS_DIR / "quotes_log.csv" # Log file path

# Helper functions

def load_quotes(path: Path):
    """Load quotes from a JSON file."""
    if not path.exists():
        raise FileNotFoundError(f"Quotes file not found: {path}")

    # Open the JSON file and parse it into Python objects
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    quotes = []

    # Each quote should be a dictionary with 'text' and 'author' keys
    for q in data:
        # we're going to be flexible with the keys
        text = q.get("text") or q.get("quote") or q.get("q")
        author = q.get("author") or q.get("a") or "Unknown"

        if text:
            quotes.append((text.strip(), author.strip()))

    if not quotes:
        raise ValueError("No valid quotes found in quotes.json")
    
    return quotes

def pick_quote():
    """Pick a random quote from the quotes list."""
    quotes = load_quotes(QUOTES_PATH)
    return random.choice(quotes)

def log_quote(text: str, author: str):
    """Log the displayed quote to a CSV file with a timestamp."""
    new_file = not LOG_FILE.exists()

    with LOG_FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Write header if file is new
        if new_file:
            writer.writerow(["timestamp", "quote", "author"])

        # Write the current quote with timestamp and author
        writer.writerow([datetime.now().isoformat(timespec="seconds"), text, author])


def show_now() -> int:
    """Display a quote notification immediately."""
    text, author = pick_quote()
    body = f"{text}\n- {author}"

    # Show the notification
    ok = notify(TITLE, body)

    # Log the quote even if notification fails
    log_quote(text, author)
    # Return 0 if notification was successful, else 1
    return 0 if ok else 1

def is_windows() -> bool:
    """ Check if the operating system is Windows."""
    return sys.platform.startswith("win")

def win_install_task(hhmm: str):
    """Install the script as a daily scheduled task on Windows."""
    if not is_windows():
        print("Scheduled task installation is only supported on Windows.")
        return 1
    
    # Make sure the time string is valid
    try:
        datetime.strptime(hhmm, "%H:%M")
    except ValueError:
        print("Time must be in 24-hour HH:MM format, e.g., 09:00 for 9 AM.")
        return 1

    # Use the currenmt Python interpreter to run the script
    python_exe = sys.executable
    script_path = str((ROOT / "daily_quote.py").resolve())

    # Try to use pythonw.exe for silent execution if available
    if python_exe.lower().endswith("python.exe"):
        candidate = python_exe[:-9] + "pythonw.exe"
        if Path(candidate).exists():
            python_exe = candidate
    
    task_name = APP_NAME

    # Build the schtasks command
    # /SC DAILY means the task runs daily
    # /ST specifies the start time
    # /TR specifies the task to run
    cmd = (
        f'schtasks /Create /TN "{task_name}" /SC DAILY /ST {hhmm} '
        f'/TR "\"{python_exe}\" \"{script_path}\" --now" /F'
    )

    try:
        completed = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True
        )

        if completed.returncode == 0:
            print(f"Scheduled task '{task_name}' set for {hhmm}.")
            return 0
        else:
            print("Failed to create scheduled task. Output:\n" +
                  completed.stdout + completed.stderr)
            return completed.returncode
    except Exception as e:
        print(f"Error while creating scheduled task: {e}")
        return 1
 
def main():
    """
    Parse command line arguments and execute the appropriate action.
    """
    parser = argparse.ArgumentParser(
        description = "Daily Quote Notifier"
    )

    # --now : show a quote notification immediately
    parser.add_argument(
        "--now",
        action = "store_true",
        help = "Show a quote notification immediately"
    )

    # --install HH:MM schedule daily task at specified time
    parser.add_argument(
        "--install",
        metavar = "HH:MM",
        help = "Install as a daily scheduled task at specified time (24-hour format)"
    )

    args = parser.parse_args()

    # Default return code
    rc = 0

    # If the user passed --now, show a quote immediately
    if args.now:
        rc = show_now()

    # If the user passed --install, create/update the scheduled task
    if args.install:
        rc = win_install_task(args.install)
    
    # If no arguments were passed, just show a quote
    if not args.now and not args.install:
        rc = show_now()

    # Exit the script with this status code (0 = success)
    raise SystemExit(rc)

# This makes sure main() runs only when this script is executed directly
# Not when it is imported from somewhere else
if __name__ == "__main__":
    main()
