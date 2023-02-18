# mdb-E_S-file-system

This is a simple python script for getting from *.mdb file and sending data via FTP.
Also, it can create a windows scheduler's task if it needed.


## Installing using Github
```shell
git clone https://github.com/taras-andruschenko/mdb-E_S-file-system.git
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
#### to get and send only today's data:
```shell
python file_sender.py
```
#### to get and send all data:
```shell
python file_sender.py -all
```

#### to create an .exe file:
```shell
pyinstaller --onefile --add-data "data_extractor.py;." file_sender.py
```
Locate the executable:
Once PyInstaller has finished creating the executable, 
you can find it in the `dist` folder that is created in the same directory as your script


#### Implemented features
1. Sending files via FTP
2. Command for packing script into .exe file
3. Adding a task to Windows Scheduler if it needed

#### Problems solved
1. Fixed SQL queries
2. Added flag `-all`, which allows to get all data from db_table
3. Fixed the name of sended file

#### Unsolved problems
1. `-savefiles` flag wasn't added because it's unnecessary.
2. Solution wasn't tested because of problems with accessing to db.