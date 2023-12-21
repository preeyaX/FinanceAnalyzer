"""
Parent class of all the pages in the application.
- Includes features common to all pages: header, linked list pointers, Tkinter displays.
- Has 6 child classes (each of the 6 pages in the application)
"""

from tkinter import *
from Company import *

# Pages is the parent class of all the pages present in the application
class Pages:

    def __init__(self, window, padx, pady, w = 1440, h = 900):
        self.page = Frame(window, width = w, height = h)
        self.header = Frame(window, bg = "#D7F0FF", width = w, height = 50)
        self.padx = padx
        self.pady = pady
        self.company_id = 0

    def getHeader(self):
        return (self.header)
    
    def getPage(self):
        return (self.page)

    def display_page(self):
        self.getHeader().pack(side = TOP, fill = X)
        self.getPage().pack(padx = self.padx, pady = self.pady, expand = TRUE)
    
    def hide_page(self):
        self.getHeader().pack_forget()
        self.getPage().pack_forget()
    
    # Setting up the linked list.
    def setNextPage(self, next_page):
        self.next = next_page
    
    def setNextPage2(self, next_page):
        self.next2 = next_page

    def setPrevPage(self, prev_page):
        self.prev = prev_page

    def getNextPage(self):
        return (self.next)
    
    def getNextPage2(self):
        return (self.next2)
    
    def getPrevPage(self):
        return (self.prev)
    