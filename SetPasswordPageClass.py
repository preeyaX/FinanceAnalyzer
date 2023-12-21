"""
PAGE 1: SetPasswordPage - Page that arises during first use to set the password.
This page is a child class of Pages - inherits its properties and methods.
Functions:
- Tkinter elements on the page are created
- Linked to PasswordClass for saving the password appropriately.
- Error handling of password input.
"""


from tkmacosx.basewidgets.button_base import BUTTON_ITEMS
import PasswordClass
from tkinter import *
from tkinter.font import Font
import PagesClass
from tkmacosx import Button
import tkinter.messagebox
import config


# Page 1 - child class of "Pages" that helps in setting the password
class SetPasswordPage(PagesClass.Pages):
    
    def __p1_save_command(self):

        password1 = self.p1_password_input.get()
        password2 = self.p1_password_confirm.get()
        
        if password1 != "" and password2 != "":
            
            if password1 == password2:
                bool = PasswordClass.Password.validatePassword(password2)
                
                if bool == TRUE:
                    hashed = PasswordClass.Password.hashPassword(password2)
                    PasswordClass.Password.saveToDb(config.DATABASE_PATH, hashed)

                    self.hide_page()
                    self.getNextPage().paint_page()
                    self.getNextPage().display_page()

                else:
                    tkinter.messagebox.showinfo("Invalid Password", "Ensure password has letters, numbers, and symbols.")
            else:
                tkinter.messagebox.showinfo("No Match", "Please ensure that both entry fields have the same password.")
        else:
            tkinter.messagebox.showinfo("Fill Both Fields", "You must enter the password both in both fields to continue.")

    
    def __toggle_password(self, input, button):
        if input.cget("show") == "":
            input.config(show = "*")
            button.config(text = "Show")
        else:
            input.config(show = "")
            button.config(text = "Hide")

    def paint_page(self):

        # TEXT WIDGETS
        # "Welcome to Finance Analyzer."
        self.p1_welcome_label = Label(self.getPage(), text = "Welcome to Finance Analyzer.", font = Font(family = "Helvetica Neue", size = 57))
        self.p1_welcome_label.grid(row = 0, column = 0, columnspan = 2)
        # "Set a password to ensure confidentiality."
        self.p1_set_password_label = Label(self.getPage(), text = "Set a password to ensure data confidentiality.", font = Font(family = "Helvetica Neue", size = 35))
        self.p1_set_password_label.grid(row = 1, column = 0, pady = 30, columnspan = 2)


        # ENTER PASSWORD WIDGETS
        # "Enter your password:"
        self.p1_enter_password_label = Label(self.getPage(), text = "Enter your password:", font = Font(family = "Helvetica Neue", size = 25))
        self.p1_enter_password_label.grid(row = 2, column = 0, columnspan = 2)
        # Password input
        self.p1_password_input = Entry(self.getPage(), width = 20, fg = "black", show = "*", font = Font(family = "Helvetica Neue", size = 18))
        self.p1_password_input.grid(row = 3, column = 0, pady = 15, sticky = E)
        # show/hide buttons:
        self.p1_show_hide_button1 = Button(self.getPage(), text = "Show", font = Font(family = "Helvetica Neue", size = 18), 
                            borderless = True, fg = "#525252", width = 57, height = 33,
                            command = lambda: self.__toggle_password(self.p1_password_input, self.p1_show_hide_button1))
        self.p1_show_hide_button1.grid(row = 3, column = 1, sticky = W)


        # CONFIRM PASSWORD WIDGETS
        # "Confirm password:"
        self.p1_confirm_password_label = Label(self.getPage(), text = "Confirm the password:", font = Font(family = "Helvetica Neue", size = 25))
        self.p1_confirm_password_label.grid(row = 4, column = 0, pady = 15, columnspan = 2)
        # Password confirm
        self.p1_password_confirm = Entry(self.getPage(), width = 20, fg = "black", show = "*", font = Font(family = "Helvetica Neue", size = 18))
        self.p1_password_confirm.grid(row = 5, column = 0, sticky = E)
        # show/hide buttons:
        self.p1_show_hide_button2 = Button(self.getPage(), text = "Show", font = Font(family = "Helvetica Neue", size = 18), 
                            borderless = True, fg = "#525252", width = 57, height = 33,
                            command = lambda: self.__toggle_password(self.p1_password_confirm, self.p1_show_hide_button2))
        self.p1_show_hide_button2.grid(row = 5, column = 1, sticky = W)


        # SAVE BUTTON WIDGET
        self.p1_save_button = Button(self.getPage(), text = "SAVE", width = 290, height = 30, bg = "#00A3FF", fg = "white", 
                    font = Font(family = "Helvetica Neue", size = 20), command = lambda: self.__p1_save_command())
        self.p1_save_button.grid(row = 6, column = 0, columnspan = 2, pady = 15)

