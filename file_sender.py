import ftplib

import win32com.client
import tkinter as tk

from data_extractor import extract_data_to_csv_file


def add_daily_sync_task():
    # Create a new Task Scheduler object
    scheduler = win32com.client.Dispatch("Schedule.Service")
    scheduler.Connect()

    # Create a new task
    task = scheduler.NewTask(0)

    # Set the task settings
    task.RegistrationInfo.Description = "TEST_TASK!"
    task.Settings.Enabled = True

    # Set the task trigger to run every day at 6:00 AM
    trigger = task.Triggers.Create(2)
    trigger.StartBoundary = "2023-02-19T06:00:00"
    trigger.DaysInterval = 1

    # Set the task action to run the sync.py script
    action = task.Actions.Create(0)
    action.Path = "python"  # TODO: add the correct path
    action.Arguments = "sync.py"  # TODO: add sync.py

    # Add the task
    folder = scheduler.GetFolder("\\")
    task_registered = folder.RegisterTaskDefinition("TEST_TASK!", task, 6, "", "", 3)

    if task_registered:
        print('Task registered successfully.')
    else:
        print('Failed to register task.')


def add_task_prompt():
    # Create a new Tkinter window
    window = tk.Tk()
    window.title('Add Task')

    # Add a label with the prompt
    prompt = tk.Label(window, text='Please confirm adding the daily sync task to the Windows Scheduler')
    prompt.pack(pady=10)

    # Add a "Yes" button that calls the add_daily_sync_task() function
    yes_button = tk.Button(window, text='Yes', command=add_daily_sync_task)
    yes_button.pack(side=tk.LEFT, padx=10)

    # Add a "No" button that closes the window
    no_button = tk.Button(window, text='No', command=window.destroy)
    no_button.pack(side=tk.RIGHT, padx=10)

    # Display the window and wait for the user's response
    window.mainloop()


def main():
    # Call the add_task_prompt() function to display the prompt
    add_task_prompt()

    # Define FTP server details
    ftp_server = "ftp.dash-ipostnet.com"
    ftp_username = "manifest_file_upload@dash-ipostnet.com"
    ftp_password = "SC{{m@$PZ2;L"  # This is bad practice! Password must be hidden =)
    ftp_directory = "/"

    # Extract data and create new csv file and define local file path/name
    file_path = extract_data_to_csv_file()
    filename = file_path[file_path.rfind("\\") + 1:]

    # Connect to FTP server with TLS
    ftp = ftplib.FTP_TLS()
    ftp.set_debuglevel(2)
    ftp.connect(ftp_server)
    ftp.login(user=ftp_username, passwd=ftp_password)

    # Open local file and send to FTP server
    with open(file_path, "rb") as file:
        ftp.storbinary(f"STOR /{filename}", file)
    ftp.close()
    print("Done")


if __name__ == '__main__':
    main()
