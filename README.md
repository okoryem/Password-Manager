# Password Manager

This Password Manager is a secure and user-friendly application built using Python and `customtkinter`. It allows users to securely store, retrieve, modify, and delete passwords and related information in an encrypted database using `SQLCipher`.

## Features

- **Set a Master Password**: First-time users are required to set a master password, which encrypts the database and ensures data security.
- **Add Passwords**: Store passwords with associated information such as website and username.
- **Retrieve Passwords**: View saved passwords and their details in a secure manner.
- **Modify Passwords**: Update existing password entries with new information.
- **Delete Passwords**: Permanently delete password entries.
- **Encrypted Storage**: All passwords are stored in an encrypted SQLite database (`SQLCipher`).

## Requirements

- Python 3.x
- `customtkinter`
- `sqlite3`
- `pysqlcipher3`
- `python-dotenv`

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required packages:
   ```bash
   pip install customtkinter pysqlcipher3 python-dotenv
   ```

3. Create a `.env` file for the master key:
   - The app will generate a `key.env` file to store the master password on first use.

4. Run the application:
   ```bash
   python app.py
   ```

## Usage

1. **First-Time Setup**:
   - On the first run, you will be prompted to set a master password. This password encrypts and secures the database.
   - Restart the application after setting the master password.

2. **Main Features**:
   - Add a new password by entering details in the input fields and selecting "Add Password."
   - View saved passwords by selecting "Retrieve Information."
   - Update existing passwords using "Change Information."
   - Delete passwords by choosing "Delete Information."

3. **Navigation**:
   - Use the dropdown menu to switch between actions (Add, Retrieve, Change, or Delete Password).
   - Password entries are displayed as buttons in the application. Click a button to view, modify, or delete its details based on the selected action.

## Media

Below are visual examples of how the application works:

### Screenshots

1. **Set Master Password**
   - Displays the interface for setting the master password.
   - ![Uploading Screen Shot 2025-01-11 at 6.12.21 PM.png…]()
   - <img width="312" alt="Screen Shot 2025-01-11 at 6 12 55 PM" src="https://github.com/user-attachments/assets/5570b9f4-505f-4539-8304-beb82d387d93" />
   
   



2. **Get Master Password**
   - Shows the prompt for entering the master password to access the application.

3. **Main Window (No Passwords)**
   - The main interface when no passwords are stored.

4. **Main Window (With Passwords)**
   - The main interface displaying stored passwords as buttons.

5. **Password Info Popup**
   - Shows the popup with details of a specific password entry.

### Video Demonstration

- A walkthrough video demonstrating the app's features and functionality will be included.

## Security Notes

- The master password is stored locally in an environment file (`key.env`). Ensure this file is secure.
- The SQLite database (`passwords.db`) is encrypted using `SQLCipher` with the master password as the key.

## Contributions

Feel free to fork this repository and contribute to its development by submitting pull requests. Any feedback or suggestions are welcome!

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- Built using `customtkinter` for a modern, user-friendly interface.
- Utilizes `SQLCipher` for encrypted database management.
- Inspired by the need for simple, secure password management tools.

