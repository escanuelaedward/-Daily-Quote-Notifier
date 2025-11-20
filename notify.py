# This file will contain the notification function used by the main script
# The goals is to show a pop-up notification on Windows
# If Windows toast (toast is what the pop-up is called) we will try a different method

def notify(title: str, message: str, *, duration: int = 6) -> bool:

    # Native Windows Toast
    # Thesse are the normal pop-ups you see on Windows
    # win10toast library lets Python acces the Windows notification system

    try:
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast(
            title,
            message,
            duration = duration,
            threaded = False    # This just means to block until the pop-up finishes
        )
        return True
    except Exception:
        # if this fails we try the next method
        pass

    # Back up for the first method if user isn't using Windows 10 or higher
    try:
        from plyer import notification
        notification.notify(
            title = title,
            message = message,
            timeout = duration
        )
        return True
    except Exception:
        pass

    # Finally if both methods fail we try to print something for the user to see
    try:
        print(f"[NOTIFICATION] {title}: {message}")
        return True
    except Exception:
        return False
