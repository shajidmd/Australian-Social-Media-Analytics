-------------------------Uploading Aurin dataset to CouchDB--------------------------------------
For the ease of transferring data, we used FileZilla for file transfer.
Steps 
1.	Download FileZilla
2.	SFTP connection to the VM
3.	Click the menu options
4.	FileZilla OR Edit -> Settings OR Preferences -> Connection -> SFTP
5.	Click Add key file and navigate to the folder storing cloudkey
6.	Convert cloudkey file to ppk format.
7.	Open File -> Site Manager .
8.	Click New Site and give it a name.
9.	Insert the IP address of the instance as Host.
10.	Logon Type is interactive
11.	The user is 'ubuntu' 
12.	Click Connect

The left side of the FileZilla window will list the files of your computer. The right side will contain the folders and files on the VM.

1.	Log in to instance1 and make the disk writable
2.	sudo chown ubuntu /volume
3.	Navigate to data storage directory in the right side of the FileZilla screen.
4.	Drag and drop aurin dataset files (json zip files) from local computer to the VM.
5.	sudo unzip <json.zip> /extracted_files
6.	sudo rm meta*
7.	python3 move_data_to_couchdb.py

