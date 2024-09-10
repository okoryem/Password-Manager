import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, END
from customtkinter import CTkFont
#from password_class import Information, HashMapPassword
import pysqlcipher3.dbapi2 as sqlite
import json, os, sys
from dotenv import load_dotenv, set_key



load_dotenv("key.env")
KEY = os.getenv('KEY')

class Information:
    def __init__(self, name, website, username, password):
        self.name = name
        self.website = website
        self.username = username
        self.password = password

        self.information = {
            "name": name,
            "website" : website,
            "username" : username,
            "password" : password
        }

    def getName(self):
        return self.name

    def getWebsite(self):
        return self.website

    def getUsername(self):
        return self.username

    def getPassword(self):
        return self.password
    
    def setName(self, name):
        self.name = name
        self.information["name"] = name

    def setWebsite(self, website):
        self.website = website
        self.information["website"] = website

    def setUsername(self, username):
        self.username = username
        self.information["username"] = username

    def setPassword(self, password):
        self.password = password
        self.information["password"] = password

    def getDict(self):
        return self.information

# Button class
class PasswordButton():
    def __init__(self, title, frame, website, username, password):
        self.title = title
        self.frame = frame
        self.website = website
        self.username = username
        self.password = password

        # Configs of a button
        self.newbutton = ctk.CTkButton(frame, text=(f"{title}"), width=580, height=100, font=('Modern', 40), fg_color="#F4F4FB", text_color="#000000",command=lambda: self.checkStatus())
        self.newbutton.pack(expand=True, fill="x", padx=10, pady=5)


    def getTitle(self):
        return self.title
    
    def getWebsite(self):
        return self.website
    
    def getUsername(self):
        return self.username
    
    def getPassword(self):
        return self.password
    
    def setTitle(self, new_title):
        self.title = new_title

    def setWebsite(self, new_website):
        self.website = new_website

    def setUsername(self, new_username):
        self.username = new_username

    def setPassword(self, new_password):
        self.password = new_password

    def setText(self, new_title):
        self.newbutton.configure(text=f"{new_title}")

    # Command of the button to check the status of the choicebox
    def checkStatus(self):
        # Reference to choicebox
        choice = self.frame.master.master.master.master.master.choiceBox.get()

        if choice == "Delete Information":
            self.deleteInfo()

        elif choice == "Change Information":
            self.changeInfo()

        else:
            self.displayInfo()
    
    def displayInfo(self):
        name = self.getTitle()

        conn = sqlite.connect("passwords.db")
        conn.execute(f"PRAGMA key = '{KEY}';")
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM passwords WHERE password_name = ?", (name,))

        result = cursor.fetchone()

        if result is not None:
            cursor.execute(f"SELECT password_information FROM passwords WHERE password_name =?", (name,))

            # Gets data and converts it into a python dictionary from a json
            json_data = cursor.fetchone()[0]
            loadedInformation = json.loads(json_data)

            conn.commit()
            conn.close()

            # Creates password object with loaded information
            passwordInformation = Information(loadedInformation['name'], loadedInformation['website'], loadedInformation['username'], loadedInformation['password'])

            messagebox.showinfo(f"{passwordInformation.getName()}", f"Website: {passwordInformation.getWebsite()}\nUsername: {passwordInformation.getUsername()}\nPassword: {passwordInformation.getPassword()}")
        else:
            messagebox.showerror("Password does not exist", f"{name} does not exist")

            conn.commit()
            conn.close()

    def deleteInfo(self):
        name = self.getTitle()
        
        conn = sqlite.connect("passwords.db")
        conn.execute(f"PRAGMA key = '{KEY}';")
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM passwords WHERE password_name = ?", (name,))

        result = cursor.fetchone()

        if result is not None:
            answer = messagebox.askyesno(None, f"Are you sure you want to delete: {name}?")

            # Checks if answer is yes
            if answer == 1:
                conn = sqlite.connect("passwords.db")
                conn.execute(f"PRAGMA key = '{KEY}';")
                cursor = conn.cursor()

                self.newbutton.destroy()

                cursor.execute(f"DELETE FROM passwords WHERE password_name = ?", (name,))

                conn.commit()
                cursor.close()
                conn.close()
        else:
            messagebox.showerror("Password does not exist", f"{name} does not exist")

            conn.commit()
            conn.close()



    def changeInfo(self):
        # References from entry boxes
        new_name = self.frame.master.master.master.master.master.password_new_name.get()
        name = self.frame.master.master.master.master.master.password_name.get()
        website = self.frame.master.master.master.master.master.password_website.get()
        username = self.frame.master.master.master.master.master.password_username.get()
        password = self.frame.master.master.master.master.master.password_password.get()

        # Checks that all entry boxes are filled
        if new_name and name and website and username and password:
            conn = sqlite.connect("passwords.db")
            conn.execute(f"PRAGMA key = '{KEY}';")
            cursor = conn.cursor()

            cursor.execute("SELECT 1 FROM passwords WHERE password_name = ?", (name,))

            result = cursor.fetchone()

            if result is not None:
                cursor.execute("SELECT 1 FROM passwords WHERE password_name = ?", (new_name,))
                result_new = cursor.fetchone()

                if result_new is None:

                    # Creates information object with information from entry boxes
                    newInformation = Information(new_name, website, username, password)

                    # Turns information into a json
                    json_data = json.dumps(newInformation.getDict())

                    conn = sqlite.connect("passwords.db")
                    conn.execute(f"PRAGMA key = '{KEY}';")
                    cursor = conn.cursor()

                    cursor.execute("""UPDATE passwords SET password_information = ?, password_name = ? WHERE password_name = ?""", (json_data, new_name, name))

                    conn.commit()
                    conn.close()

                    self.setTitle(new_name)
                    self.setWebsite(website)
                    self.setUsername(username)
                    self.setPassword(password)
                    self.newbutton.configure(text=f"{new_name}")

                else:
                    messagebox.showerror("Password already exist", f"{new_name} already exist")
                    conn.commit()
                    conn.close()
            else:
                messagebox.showerror("Password does not exist", f"{name} does not exist")
                conn.commit()
                conn.close()
                

        else:
            messagebox.showerror("Input Error", "Please Fill Out All Entries")


class PasswordApp():
    
    def __init__(self):
        global KEY
        load_dotenv("key.env")
        KEY = os.getenv('KEY')

        self.root = tk.Tk()
        self.root.withdraw()


        if not os.path.isfile("passwords.db") and not KEY:
            answer = messagebox.askokcancel("Welcome", "Thank you for using Password Manager. In order you use the application you must set up a master password.")
            if answer == 1:
                self.showSetMasterPasswordWindow()
                self.showMasterPasswordWindow()
                self.showMainWindow()
            else:
                sys.exit()
        else:
            self.showMasterPasswordWindow()
            self.showMainWindow()


    def showSetMasterPasswordWindow(self):
        self.setMaster = ctk.CTkToplevel()
        self.setMaster.title("Set Master Password")
        self.setMaster.geometry("300x300")

        self.setMasterFrame = ctk.CTkFrame(self.setMaster, fg_color="#111759")
        self.setMasterFrame.pack(expand=True, fill="both")

        self.setMasterPasswordTitle = ctk.CTkLabel(self.setMasterFrame, text="Set Master Password", font=ctk.CTkFont(family="Helvetica", size=20, weight="bold"), text_color="#F4F4FB")
        self.setMasterPasswordTitle.pack(expand=True, fill="both", padx=5, pady=5)

        self.setMasterPassword = ctk.CTkEntry(self.setMasterFrame, placeholder_text="Master Password", border_color="#23296B", fg_color="transparent", text_color="#969CDD", placeholder_text_color="#969CDD")
        self.setMasterPassword.pack(expand=True, fill="both", padx=10, pady=5)

        self.retypeMasterPassword = ctk.CTkEntry(self.setMasterFrame, placeholder_text="Re-Type Master Password", border_color="#23296B", fg_color="transparent", text_color="#969CDD", placeholder_text_color="#969CDD")
        self.retypeMasterPassword.pack(expand=True, fill="both", padx=10, pady=5)

        self.setMasterPasswordButton = ctk.CTkButton(self.setMasterFrame, text="Set Password", font=("Helvetica", 18), corner_radius=32, fg_color="#F4F4FB", text_color="#111759",command=self.checkMatchingPassword)
        self.setMasterPasswordButton.pack(expand=True, fill="both", padx=10, pady=10)


        self.setMaster.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))



    def checkMatchingPassword(self):
        password1 = self.setMasterPassword.get().strip()
        password2 = self.retypeMasterPassword.get().strip()

        if password1 and password2:

            if password1 != password2:
                messagebox.showerror("Passwords Don't Match", "Passwords Don't Match")
            else:
                global KEY
                env_file = "key.env"
                '''
                clean_password = password1.replace('"', '').replace("'", "")
                with open(env_file, 'w') as file:
                    file.write(f"KEY={clean_password}\n")
                '''
                set_key(env_file, "KEY", password1)
                load_dotenv(env_file)
                self.setMaster.destroy()
                self.showMasterPasswordWindow()
                KEY = password1
        else:
            messagebox.showerror("Input Error", "Please Fill Out All Entries")

    def showMasterPasswordWindow(self):
        self.getMaster = ctk.CTkToplevel()
        self.getMaster.title("Get Master Password")
        self.getMaster.geometry("300x300")

        self.getMasterFrame = ctk.CTkFrame(self.getMaster, fg_color="#111759")
        self.getMasterFrame.pack(expand=True, fill="both")

        self.masterPasswordTitle = ctk.CTkLabel(self.getMasterFrame, text="Enter Your Master Password", font=ctk.CTkFont(family="Helvetica", size=20, weight="bold"), text_color="#F4F4FB")
        self.masterPasswordTitle.pack(expand=True, fill="both", padx=5, pady=5)

        self.masterPassword = ctk.CTkEntry(self.getMasterFrame, placeholder_text="Master Password", border_color="#23296B", fg_color="transparent", text_color="#969CDD", placeholder_text_color="#969CDD")
        self.masterPassword.pack(expand=True, fill="both", padx=10, pady=5)

        self.masterPasswordButton = ctk.CTkButton(self.getMasterFrame, text="Enter", font=("Helvetica", 18), corner_radius=32, fg_color="#F4F4FB", text_color="#111759",command=self.checkPassword)
        self.masterPasswordButton.pack(expand=True, fill="both", padx=10, pady=10)

        self.getMaster.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))

        if hasattr(self, 'setMaster') and self.setMaster.winfo_exists():
            self.getMaster.withdraw()
        else:
            self.getMaster.deiconify()


    def checkPassword(self):
        global KEY

        '''
        new_env_file = "key.env"
        load_dotenv(new_env_file)
        KEY = os.getenv('KEY')
        '''
        enteredPassword = self.masterPassword.get()

        if enteredPassword != KEY:
            messagebox.showerror("Incorrect Password", "Incorrect Password")

        else:
            self.getMaster.destroy()
            self.showMainWindow()





                    
    def showMainWindow(self):

        if KEY:
            conn = sqlite.connect("passwords.db")
            conn.execute(f"PRAGMA key = '{KEY}';")
            cursor = conn.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                password_name text,
                password_information text
            )""")
            
            conn.commit()
            conn.close()

        
        # Dictionary of all buttons
        self.buttonMap = {}

        # Sets apperance (dont think it matters for my app as it is one color)
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        # Creates window
        self.window = ctk.CTk()

        WIDTH = 600
        HEIGHT = 600

        self.window.geometry(f"{WIDTH}x{HEIGHT}")
        self.window.title("Password Manager")

        my_font = ctk.CTkFont(family="Helvetica", size=20, weight="bold")

        # Creates master frame (black background)
        self.masterFrame = ctk.CTkFrame(self.window, fg_color="#111759")
        self.masterFrame.pack(expand=True, fill="both")

        # Creates frame containing inputFrame and choiceFrame
        self.mainFrame = ctk.CTkFrame(self.masterFrame, fg_color="transparent")
        self.mainFrame.pack(side="left", expand=True, fill="x", padx=20, pady=5)

        # Creates frame holding title, entry boxes, button, and drop down bar
        self.inputFrame = ctk.CTkFrame(self.mainFrame, fg_color="#23296B")
        self.inputFrame.pack(expand=True, fill="both", padx=5, pady=5)

        # Creates title label
        self.title = ctk.CTkLabel(self.inputFrame, text="Password Manager", font=my_font, text_color="#F4F4FB")
        self.title.pack(expand=True, fill="both", padx=5, pady=5)

        # Creates choice frame that holds password buttons
        self.choiceFrame = ctk.CTkScrollableFrame(self.mainFrame, fg_color="#23296B", scrollbar_button_color="#F4F4FB", )
        self.choiceFrame.pack(expand=True, fill="both", padx=5, pady=5)

        if KEY:
            conn = sqlite.connect("passwords.db")
            conn.execute(f"PRAGMA key = '{KEY}';")
            cursor = conn.cursor()

            # Grabs all password data from database
            cursor.execute("SELECT *, oid FROM passwords")
            passwords = cursor.fetchall()

            # Creates the buttons for all the existing data
            def loadButtons():
                for password in passwords:
                    password_name = password[0]
                    json_data = password[1]

                    # Loads the password data that was a json and it is converted back into a python dictionary
                    loadedInformation = json.loads(json_data)

                    # Turns data into an Information object
                    passwordInformation = Information(loadedInformation['name'], loadedInformation['website'], loadedInformation['username'], loadedInformation['password'])
                    
                    name = passwordInformation.getName()
                    website = passwordInformation.getWebsite()
                    username = passwordInformation.getUsername()
                    password = passwordInformation.getPassword()

                    # Creates button with varibales and place them in choiceFrame
                    button = PasswordButton(name, self.choiceFrame, website, username, password)

                    #Adds Button to button dicitonary
                    self.buttonMap[name] = button

                conn.commit()
                conn.close()

            loadButtons()

        # Non Existing entry box
        self.password_new_name = None

        # Changes aspects of the app based on the mode selected
        def functionEditor(choice):
            self.mainButton.configure(text=choice)

            if choice == "Delete Information":
                self.mainButton.configure(fg_color="red")
                for button in self.buttonMap.values():
                    button.newbutton.configure(fg_color="red")
            elif choice == "Change Information":
                if self.password_new_name is None:                
                    self.password_new_name = ctk.CTkEntry(self.inputFrame, placeholder_text="New Password Name", border_color="#23296B", fg_color="transparent", text_color="#969CDD", placeholder_text_color="#969CDD")
                    self.password_new_name.pack(before=self.password_website, expand=True, fill="both", padx=10, pady=5)
                    self.window.password_new_name = self.password_new_name
                self.mainButton.configure(fg_color="#F4F4FB")
                for button in self.buttonMap.values():
                    button.newbutton.configure(fg_color="#F4F4FB")
            else:
                if self.password_new_name is not None:
                    self.password_new_name.destroy()
                    self.password_new_name = None
                self.mainButton.configure(fg_color="#F4F4FB")
                for button in self.buttonMap.values():
                    button.newbutton.configure(fg_color="#F4F4FB")


        self.choices = ["Add Password", "Retrieve Information", "Change Information", "Delete Information"]
        
        # Creates the choicebox
        self.choiceBox = ctk.CTkComboBox(self.inputFrame, fg_color="#2A3072", border_color="#23296B",values=self.choices, command=functionEditor, text_color="#969CDD", button_color="#F4F4FB")
        self.choiceBox.pack(side="bottom", expand=True, fill="both", padx=5, pady=10)

        # For referencing in button class
        self.window.choiceBox = self.choiceBox

        # Entry Boxes
        self.password_name = ctk.CTkEntry(self.inputFrame, placeholder_text="Password Name", border_color="#23296B", fg_color="transparent", text_color="#969CDD", placeholder_text_color="#969CDD")
        self.password_name.pack(expand=True, fill="both", padx=10, pady=5)

        self.password_website = ctk.CTkEntry(self.inputFrame, placeholder_text="Website", border_color="#23296B", fg_color="transparent", text_color="#969CDD", placeholder_text_color="#969CDD")
        self.password_website.pack(expand=True, fill="both", padx=10, pady=5)

        self.password_username = ctk.CTkEntry(self.inputFrame, placeholder_text="Username", border_color="#23296B", fg_color="transparent", text_color="#969CDD", placeholder_text_color="#969CDD")
        self.password_username.pack(expand=True, fill="both", padx=10, pady=5)

        self.password_password = ctk.CTkEntry(self.inputFrame, placeholder_text="Password", border_color="#23296B", fg_color="transparent", text_color="#969CDD", placeholder_text_color="#969CDD")
        self.password_password.pack(expand=True, fill="both", padx=10, pady=5)
        

        # For referencing in button class
        self.window.password_new_name = self.password_new_name
        self.window.password_name = self.password_name
        self.window.password_website = self.password_website
        self.window.password_username = self.password_username
        self.window.password_password = self.password_password


        # Creates the main button
        self.mainButton = ctk.CTkButton(self.inputFrame, text="Add Password", font=("Helvetica", 18), corner_radius=32, fg_color="#F4F4FB", text_color="#111759",command=self.checkStatusMain)
        self.mainButton.pack(expand=True, fill="both", padx=10, pady=10)

        if self.getMaster.winfo_exists():
            self.window.withdraw()
        else:
            self.window.deiconify()

        self.window.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))
        self.window.mainloop()


    # Checks status of choice box for main button command
    def checkStatusMain(self):
        if self.choiceBox.get() == "Add Password":
            self.create_new_button()
        elif self.choiceBox.get() == "Retrieve Information":
            self.display_button_info()
        elif self.choiceBox.get() == "Change Information":
            self.change_button_info()
        else:
            self.delete_button()

    def create_new_button(self):
        name = self.password_name.get()
        website = self.password_website.get()
        username = self.password_username.get()
        password = self.password_password.get()

        # Checks if all entry boxes are filled
        if name and website and username and password:

            conn = sqlite.connect("passwords.db")
            conn.execute(f"PRAGMA key = '{KEY}';")
            cursor = conn.cursor()

            cursor.execute("SELECT 1 FROM passwords WHERE password_name = ?", (name,))

            result = cursor.fetchone()

            if result is None:

                # Stores the information given in a new information object
                newInformation = Information(name, website, username, password)

                # Converts information into a json
                json_data = json.dumps(newInformation.getDict())

                conn = sqlite.connect("passwords.db")
                conn.execute(f"PRAGMA key = '{KEY}';")
                cursor = conn.cursor()

                '''
                Add feature that searches through database to
                see if name already exist. If it exist, ask the
                user if the want to overide it (with yes/no/cancel)
                '''

                cursor.execute("INSERT INTO passwords (password_name, password_information) VALUES (?, ?)", 
                            (newInformation.getName(), json_data))

                # Creates button with information
                button = PasswordButton(newInformation.getName(), self.choiceFrame, newInformation.getWebsite(), newInformation.getUsername(), newInformation.getPassword())
                self.buttonMap[newInformation.getName()] = button

                # Clears entry boxes
                self.password_name.delete(0, END)
                self.password_website.delete(0, END)
                self.password_username.delete(0, END)
                self.password_password.delete(0, END)

                conn.commit()
                conn.close()
            else:
                messagebox.showerror("Password already exist", f"{name} already exist")
                conn.commit()
                conn.close()
        else:
            messagebox.showerror("Input Error", "Please Fill Out All Entries")


    def delete_button(self):
        name = self.password_name.get()

        conn = sqlite.connect("passwords.db")
        conn.execute(f"PRAGMA key = '{KEY}';")
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM passwords WHERE password_name = ?", (name,))

        result = cursor.fetchone()

        if result is not None:
            answer = messagebox.askyesno(None, f"Are you sure you want to delete: {name}?")

            # Checks if answer is yes
            if answer == 1:
                conn = sqlite.connect("passwords.db")
                conn.execute(f"PRAGMA key = '{KEY}';")
                cursor = conn.cursor()

                # Destroys button
                button = self.buttonMap[name]
                button.newbutton.destroy()

                # Deletes Information from database
                cursor.execute(f"DELETE FROM passwords WHERE password_name = ?", (name,))

                conn.commit()
                cursor.close()
                conn.close()
            else:
                conn.commit()
                cursor.close()
                conn.close()
        else:
            conn.commit()
            cursor.close()
            conn.close()
        

    def change_button_info(self):
        new_name = self.password_new_name.get()
        old_name = self.password_name.get()
        website = self.password_website.get()
        username = self.password_username.get()
        password = self.password_password.get()
        # Checks that all entry boxes are filled
        if new_name and old_name and website and username and password:

            conn = sqlite.connect("passwords.db")
            conn.execute(f"PRAGMA key = '{KEY}';")
            cursor = conn.cursor()

            cursor.execute("SELECT 1 FROM passwords WHERE password_name = ?", (old_name,))

            result = cursor.fetchone()

            if result is not None:
                cursor.execute("SELECT 1 FROM passwords WHERE password_name = ?", (new_name,))
                result_new = cursor.fetchone()

                if result_new is None:

                    # Creates information object with information from entry boxes
                    newInformation = Information(new_name, website, username, password)

                    # Turns information into a json
                    json_data = json.dumps(newInformation.getDict())

                    cursor.execute("""UPDATE passwords SET password_information = ?, password_name = ? WHERE password_name = ?""", (json_data, new_name, old_name))

                    conn.commit()
                    conn.close()

                    button = self.buttonMap.pop(old_name, None)
                    if button:
                        button.newbutton.configure(fg_color="blue")
                        button.setText(f"{new_name}")
                        button.setTitle(new_name)
                        self.buttonMap[new_name] = button

                        # Clears entry boxes
                        self.password_name.delete(0, END)
                        self.password_website.delete(0, END)
                        self.password_username.delete(0, END)
                        self.password_password.delete(0, END)


                else:
                    messagebox.showerror("Password already exist", f"{new_name} already exist")
                    conn.commit()
                    conn.close()

            else:
                messagebox.showerror("Password does not exist", f"{old_name} does not exist")
                conn.commit()
                conn.close()


        else:
            messagebox.showerror("Input Error", "Please Fill Out All Entries")

    def display_button_info(self):
        name = self.password_name.get()

        conn = sqlite.connect("passwords.db")
        conn.execute(f"PRAGMA key = '{KEY}';")
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM passwords WHERE password_name = ?", (name,))

        result = cursor.fetchone()

        if result is not None:

            cursor.execute(f"SELECT password_information FROM passwords WHERE password_name =?", (name,))

            json_data = cursor.fetchone()[0]
            loadedInformation = json.loads(json_data)

            conn.commit()
            conn.close()

            # Creates password object with loaded information
            passwordInformation = Information(loadedInformation['name'], loadedInformation['website'], loadedInformation['username'], loadedInformation['password'])

            messagebox.showinfo(f"{passwordInformation.getName()}", f"Website: {passwordInformation.getWebsite()}\nUsername: {passwordInformation.getUsername()}\nPassword: {passwordInformation.getPassword()}")
        else:
            messagebox.showerror("Password does not exist", f"{name} does not exist")
            conn.commit()
            conn.close()

        
# Runs app
window = PasswordApp()