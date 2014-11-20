from Tkinter import *
from ttk import Frame, Button, Style, Separator, Label

class GUI(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
        
        self.height = 480
        self.width = 660
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

    def popup(self):
        top = Toplevel(width=600, height=400)
        top.title("Kinect View")

        msg = Message(top, text="Kinect goes here?")
        msg.pack()

        button = Button(top, text="Dismiss", command=top.destroy)
        button.pack()
        
    def initUI(self):
      
        self.parent.title("SewKinect")
        self.style = Style()
        self.style.theme_use("clam")

        self.grid()

        frame=Frame(self, relief=SUNKEN, borderwidth=1, width=480, height=640)
        frame.grid(column=2, columnspan=3, rowspan=50, sticky=E)

        get_measured= Button(self, text="Get Measured", command=self.popup, width=20)
        get_measured.grid(column=1, row=0)
        saved_mesaurements = Button(self, text=" Saved Measurements", command=self.get_measured, width=20)
        saved_mesaurements.grid(column=1, row=1)
        draft_patterns = Button(self, text="Draft Patterns", command=self.draw_form, width=20)
        draft_patterns.grid(column=1, row=2)


        quit_button = Button(self, text="Quit",
            command=self.quit, width = 20)
        quit_button.place(x=2, y=(self.height/2+60))


    def get_measured(self):
        self.place_forget()

    def draw_form(self):
        advanced = Button(self, text="Advanced")
        advanced.place(x=400, y=400)


def main():
  
    root = Tk()
    root.resizable(0,0)
    app = GUI(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  