"""
PAGE 2: LoginPage - For client login. Arises as 1st page after password has been set.
Functions:
- Linked to PasswordClass to enable login through stored password.
"""

import config
import PasswordClass
from tkinter import *
from tkinter.font import Font
import PagesClass
from tkmacosx import Button
import tkinter.messagebox


class LoginPage(PagesClass.Pages):

    def __p2_submit_command(self):
        p2_current_password_input = self.p2_password_input.get()
        enc_from_db = PasswordClass.Password.getFromDb(config.DATABASE_PATH)[0]
        enc_of_input = PasswordClass.Password.hashPassword(p2_current_password_input)

        if enc_from_db == enc_of_input:
            self.hide_page()
            self.getNextPage().paint_page()
            self.getNextPage().display_page()
        else:
            tkinter.messagebox.showinfo("Invalid Password", "This password is invalid. Please try again.")
        

    def __toggle_password(self):
        if self.p2_password_input.cget("show") == "":
            self.p2_password_input.config(show = "*")
            self.p2_show_hide_button.config(text = "Show")
        else:
            self.p2_password_input.config(show = "")
            self.p2_show_hide_button.config(text = "Hide")

    def paint_page(self):

        # TEXT WIDGETS
        # "Enter your password to access Finance Analyzer."
        self.p2_access_finance_analyzer_label = Label(self.getPage(), text = "Enter your password to access \n Finance Analyzer.",
                                        font = Font(family = "Helvetica Neue", size = 47))
        self.p2_access_finance_analyzer_label.grid(row = 0, column = 0, columnspan = 2, pady = 20)

        # ENTER PASSWORD WIDGETS
        # "Enter your password:"
        self.p2_enter_password_label = Label(self.getPage(), text = "Enter your password:", font = Font(family = "Helvetica Neue", size = 25))
        self.p2_enter_password_label.grid(row = 1, column = 0, columnspan = 2, pady = 20)
        # Password input
        self.p2_password_input = Entry(self.getPage(), width = 20, fg = "black", show = "*", font = Font(family = "Helvetica Neue", size = 18))
        self.p2_password_input.grid(row = 2, column = 0, sticky = E)
        # show/hide buttons:
        self.p2_show_hide_button = Button(self.getPage(), text = "Show", width = 57, height = 33, borderless = True, fg = "#525252", 
                            font = Font(family = "Helvetica Neue", size = 18),
                            command = lambda: self.__toggle_password())
        self.p2_show_hide_button.grid(row = 2, column = 1, sticky = W)


        # SUBMIT BUTTON
        self.p2_submit_button = Button(self.getPage(), text = "SUBMIT", width = 290, height = 30, bg = "#00A3FF", fg = "white",
                        font = Font(family = "Helvetica Neue", size = 18), command = lambda: self.__p2_submit_command())
        self.p2_submit_button.grid(row = 3, column = 0, columnspan = 2, pady = 15)
