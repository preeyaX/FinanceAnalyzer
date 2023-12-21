"""
MAIN FILE: must be executed to run the application.
- Creates the main Tkinter window.
- Creates the 6 pages in the application.
- Sets up the linked list.
- Displays the appropriate first page.
"""


import config
from tkinter import *
from SetPasswordPageClass import *
from LoginPageClass import *
from HomePageClass import *
from NewAnalysisPageClass import *
from AllGraphsPageClass import *
from SingleGraphPageClass import *
from tkmacosx import Button
import PasswordClass
import sys


def center_window(w, h):
    # get screen width and height
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2)
    y = ((hs/2) - (h/2))
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))


root = Tk()
root.title("Finance Analyzer")
w = root.winfo_screenwidth() #1440
h = root.winfo_screenheight() #900
center_window(w, h)

# Setting up all pages
password_page = SetPasswordPage(root, padx = 120, pady = 70)
login_page = LoginPage(root, padx = 120, pady = 100)
home_page = HomePage(root, padx = 80, pady = 0)
new_analysis_page = NewAnalysisPage(root, padx = 120, pady = 10)
all_graphs_page = AllGraphsPage(root, padx = 0, pady = 0)
single_graph_page = SingleGraphPage(root, padx = 50, pady = 40)


# Setting linked pages
# Next pages
password_page.setNextPage(login_page)
login_page.setNextPage(home_page)
home_page.setNextPage(all_graphs_page)
home_page.setNextPage2(new_analysis_page)
all_graphs_page.setNextPage(single_graph_page)
# Previous pages
new_analysis_page.setPrevPage(home_page)
all_graphs_page.setPrevPage(home_page)
single_graph_page.setPrevPage(all_graphs_page)



# Starting displays - setting up linked list head
try:
    password = PasswordClass.Password.getFromDb(config.DATABASE_PATH)
except:
    sys.exit("No database found.")
else:
    if password == None: # if the password has not been set
        password_page.paint_page()
        password_page.display_page()
    else: # if the password has already been set
        login_page.paint_page()
        login_page.display_page()

root.mainloop()
