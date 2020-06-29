"""
AJINKYA June 2017
"""
import os.path

from tkinter import Tk, ttk,messagebox
from tkinter import *
import tkinter as tk
import PIL 
import configparser
# from PIL import ImageTk,Image
class ConfigFile():

    
    def __init__(self):
        
        self.config_filepath ="honeypot.ini"

        file_exists = os.path.isfile(self.config_filepath) 

        if not file_exists:

            configFile = open(self.config_filepath, "w")
            configFile.write(
""" 
[default]
ports=7770,7771,7772
#ports=7775,7776,7777
host=0.0.0.0
logfile=/var/honeypot/honeypot.log
username = yourEmail
password = youMailpasswd
sender = Honeypot-Intruder-Alert
targets = a@gmail.com,b@gmail.com
"""
            )
            


        config = configparser.ConfigParser()
        config.read(self.config_filepath)

        self.ports = config.get('default', 'ports', raw=True, fallback="8080,8888,9999")
        self.host = config.get('default', 'host', raw=True, fallback="0.0.0.0")
        # log_filepath = config.get('default', 'logfile', raw=True, fallback="/var/log/nanopot.log")
        self.log_filepath = config.get('default', 'logfile', raw=True, fallback="/var/honeypot/honeypot.log")
        self.username =config.get('default', 'username', raw=True, fallback="none") 
        self.password =config.get('default', 'password', raw=True, fallback="none") 
        self.sender = config.get('default', 'sender', raw=True, fallback="HoneyPot Watchman") 
        self.targets = config.get('default', 'targets', raw=True, fallback="none") 


        # Double check ports provided
        ports_list = []
        targets_list=[]
        try:
            ports_list = self.ports.split(',')
            targets_list=self.targets.split(",")
            print(ports_list)
        except Exception as e:
            print('[-] Error parsing ports: %s.\nExiting.', self.ports)
            sys.exit(1)
    
    
    def saveConfig(self):
            configFile = open(self.config_filepath, "w")
            configFile.write(
f""" 
[default]
ports={self.ports}
#ports=7775,7776,7777
host=0.0.0.0
logfile=/var/honeypot/honeypot.log
username = {self.username}
password = {self.password}
sender = Honeypot-Intruder-Alert
targets = {self.targets}
"""                
            )
    

class Example(Frame):

    def __init__(self, parent):
        # bg = Image.open("bg.jpg")
        # background_image=ImageTk.PhotoImage(bg)
        # background_label = Label(parent, image=background_image)
        # background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.configFile=ConfigFile()


        Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("Honeypot Setup")
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.centreWindow()
        self.pack(fill=BOTH, expand=1)
        
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Exit", command=self.quit)
        # menubar.add_cascade(label="File", menu=fileMenu)

        userEmail = Label(self, text="Email Address")
        userEmail.grid(row=0, column=0, sticky=W+E)
        userPassword = Label(self, text="Email Password")
        userPassword.grid(row=1, column=0, sticky=W+E)
        ports = Label(self, text="Ports \n(comma seperated])")
        ports.grid(row=2, column=0, pady=10, sticky=W+E+N)
        clientEmails = Label(self, text="Subscribers \n(Email Addresses comma seperated)")
        clientEmails.grid(row=3, column=0, pady=10, sticky=W+E+N)
        
        self.userEmailText = Entry(self, width=20)
        self.userEmailText.grid(row=0, column=1, padx=5, pady=5, ipady=2, sticky=W+E)
        self.userEmailText.insert(0,self.configFile.username)

        self.userPasswordText = Entry(self, width=20)
        self.userPasswordText.grid(row=1, column=1, padx=5, pady=5, ipady=2, sticky=W+E)
        self.userPasswordText.insert(0,self.configFile.password)

        # self.countryVar = StringVar()
        # self.countryCombo = ttk.Combobox(self, textvariable=self.countryVar)
        # self.countryCombo['values'] = ('United States', 'United Kingdom', 'France')
        # self.countryCombo.current(1)
        # self.countryCombo.bind("<<ComboboxSelected>>", self.newCountry)
        # self.countryCombo.grid(row=2, column=1, padx=5, pady=5, ipady=2, sticky=W)
        
        self.portsText = Text(self, padx=5, pady=5, width=20, height=6)
        self.portsText.grid(row=2, column=1, padx=5, pady=5, sticky=W)
        self.portsText.insert(1.0,self.configFile.ports)

        self.eMailsText = Text(self, padx=5, pady=5, width=20, height=6)
        self.eMailsText.grid(row=3, column=1, padx=5, pady=5, sticky=W)
        self.eMailsText.insert(1.0,self.configFile.targets)
        # self.titleVar = StringVar()
        # self.titleVar.set("[User Status]")
        # Label(self, textvariable=self.titleVar).grid(
        #     row=4, column=1, sticky=W+E
        # )   # a reference to the label is not retained
        
        # title = ['Admin', 'End-user', 'Programmer']
        # titleList = Listbox(self, height=5)
        # for t in title:
        #     titleList.insert(END, t)
        # titleList.grid(row=3, column=2, columnspan=2, pady=5, sticky=N+E+S+W)
        # titleList.bind("<<ListboxSelect>>", self.newTitle)
        
        okBtn = Button(self, text="Save Configuration", width=10, command=self.onConfirm)
        okBtn.grid(row=4, column=0, padx=5, pady=3, sticky=W+E)
        closeBtn = Button(self, text="Close", width=10, command=self.onExit)
        closeBtn.grid(row=4, column=1, padx=5, pady=3, sticky=W+E)
    
    def centreWindow(self):
        w = 450
        h = 450
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def onExit(self):
        self.quit()
    
    def newCountry(self, event):
        print(self.countryVar.get())
    
    def fullChecked(self):
        if self.fullTimeVar.get() == 1:
            self.parent.title("Simple Window (full-time)")
        else:
            self.parent.title("Simple Window")
    
    def newTitle(self, val):
        sender = val.widget
        idx = sender.curselection()
        value = sender.get(idx)
        self.titleVar.set(value)
    
    def onConfirm(self):
        self.configFile.username=self.userEmailText.get()
        self.configFile.password=self.userPasswordText.get()
        self.configFile.ports=self.portsText.get("1.0",'end-1c')
        self.configFile.targets=self.eMailsText.get("1.0",'end-1c')
        self.configFile.saveConfig()
        messagebox.showinfo("Information", "Changes Added Successfully \nPlease Restart the Service to reflect changes")

def main():

 


    root = Tk()

    root.resizable(width=TRUE, height=TRUE)
    # resizable

    app = Example(root)

    # img = ImageTk.PhotoImage(Image.open("logo.jpg"))
    # panel = Label(root, image = img)
    # panel.pack(side = "bottom", fill = "both", expand = "no")

    root.mainloop()

if __name__ == '__main__':
    main()
