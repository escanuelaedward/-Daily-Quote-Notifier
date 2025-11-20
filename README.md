# Daily Quote Notifier

This is a small Python project that shows a daily motivational quote on your computer. It can also install itself as a Windows Scheduled Task so it will run every day at the time you choose. The goal of this project is to practice automation, notifications, file handling, and basic Python skills.

## What the project does

- Shows a motivational quote on your desktop  
- Picks a random quote from a JSON file  
- Uses Windows toast notifications if possible  
- Falls back to other methods if toast does not work  
- Logs every quote to a CSV file with the date and time  
- Can install itself as a daily scheduled task on Windows  
- Can uninstall the task with a PowerShell script


## How to install

1. Make sure Python is installed  
2. Open a terminal in the project folder  
3. Create a virtual environment  
python -m venv venv

4. Activate it  
venv\Scripts\activate


5. Install the required packages  
pip install -r requirements.txt

## How to use the program

### Show a quote right now
python daily_quote.py --now

### Install as a daily task on Windows

This makes the program run every day at the time you pick.  
Use the 24 hour time format.

python daily_quote.py --install 09:00

### Remove the daily task


## How to add more quotes

Open `quotes.json` and add new quotes inside the list like this:

```json
{ "text": "Your quote here", "author": "Name" }
```

