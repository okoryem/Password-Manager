Password Manager

This is a Python-based password manager with a graphical user interface (GUI) built using tkinter and customtkinter. The app allows users to securely store, retrieve, change, and delete password information. The stored data is encrypted using SQLCipher, ensuring that passwords are kept safe.


Features

Master Password Protection: A master password must be set upon first use, which is then required for accessing the password manager.
Password Management: Add, retrieve, change, and delete password entries.
User Interface: Simple GUI built with tkinter and customtkinter for ease of use.
Encryption: Password data is encrypted and stored using SQLCipher.


Installation

Prerequisites
Python 3.x

Required libraries (can be installed via pip):

pip install customtkinter pysqlcipher3 python-dotenv


Setting Up the Project
Clone the repository:

git clone https://github.com/your-username/password-manager.git
cd password-manager


Key Setup:
The project includes a key.env file that stores the encryption key (KEY) for the SQLCipher database. By default, this file contains an empty key. Upon first running the application, you will be prompted to set a master password. This password will be used as the encryption key and stored in the key.env file.

Run the application:

python password_manager.py


Master Password Setup:
When running the app for the first time, you'll be asked to set up a master password. This password will be stored securely in the key.env file and used to encrypt/decrypt the database.


How to Use
Run the Application:

Run the Python script to start the application:

python password_manager.py


Set Master Password:
Upon first launch, you will be prompted to set a master password. This password will be used to unlock the encrypted password database in future sessions.

Add New Passwords:
Fill in the password details (name, website, username, and password) and click Add Password to store the information securely.

Retrieve Passwords:
Select the "Retrieve Information" option, input the password name, and the password manager will display the stored details.

Change Password Information:
Select "Change Information", update the necessary details, and the new information will replace the old data.

Delete Passwords:
Select "Delete Information", input the password name, and confirm to remove the password from the database.

File Structure
password_manager.py: Main application file that handles the GUI, password management, and database operations.
passwords.db: Encrypted SQLite database that stores all passwords.
key.env: Environment file where the master password is stored (encrypted). This file will be updated with the key after you set your master password.


Technologies Used
Python: Core programming language.
tkinter & customtkinter: Libraries for creating the graphical user interface.
SQLCipher: Used for encrypting the SQLite database.
dotenv: Used to manage environment variables for securely storing the master password.

Contributing
Feel free to fork this repository and contribute to the project by submitting a pull request.


