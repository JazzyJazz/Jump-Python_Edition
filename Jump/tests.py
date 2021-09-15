import tkinter as tk
from tkinter.constants import X, Y

class ToolTip(object):
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltipwindow = self.tw = tk.Label(self.widget)
        

        def enter(event):
            self.showTooltip()
        def leave(event):
            self.hideTooltip()

        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)

    def showTooltip(self):
        self.tooltipwindow = self.tw = tk.Label(self.widget)
        self.tw.pack()
        print(1)

    def hideTooltip(self):
        self.tw.destroy()
        self.tooltipwindow = None
    
root = tk.Tk() 

your_widget = tk.Button(root, text = "Hover me!")
your_widget.pack()
ToolTip(your_widget, text = "Hover text!")