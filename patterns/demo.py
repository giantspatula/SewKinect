#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode Tkinter tutorial

In this script, we use the grid
manager to create a more complicated
layout.

author: Jan Bodnar
last modified: December 2010
website: www.zetcode.com
"""

from Tkinter import Tk, Text, BOTH, W, N, E, S
from ttk import Frame, Button, Label, Style


class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)  
        self.width = 700
        self.height = 480
         
        self.parent = parent
        self.initUI()
        self.centerWindow()

    def centerWindow(self):
      
        w = self.width
        h = self.height

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        
        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
    def initUI(self):
      
        self.parent.title("Windows")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        # self.columnconfigure(1, pad=2)
        # self.columnconfigure(3)
        # self.rowconfigure(3, weight=1)
        # self.rowconfigure(5, pad=7)
        
        area = Text(self)
        area.grid(row=1, column=2, columnspan=2, rowspan=4, 
             sticky=E+W+S+N)
        
        abtn = Button(self, text="Activate")
        abtn.pack()

        cbtn = Button(self, text="Close")
        cbtn.pack()
        
        # hbtn = Button(self, text="Help")
        # hbtn.grid(row=5, column=0,)

        obtn = Button(self, text="OK")
        obtn.grid(row=5, column=3)        
              

def main():
  
    root = Tk()
    # root.geometry("350x300+300+300")
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  