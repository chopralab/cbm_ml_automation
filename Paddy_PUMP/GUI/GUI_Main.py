import sys
import os
import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import subprocess

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Wizard(tk.Tk):
    """
    Key variables:

    """
    def __init__(self):
        tk.Tk.__init__(self)
        self.make_dir = None
        self.paddy_iteration = None
        self.working_dir = None
        self.pickle_path = None
        self.recover_bool = None
        self.savedir = None
        self.dir_path = None
        self.done_label = None
        self.recover_file_selected = None


        self.large_font = font.Font(family='TkCaptionFont', size=20, weight='bold')
        self.med_font = font.Font(family='TkCaptionFont', size=16, weight='bold')

        self.minsize(670,300)
        self.maxsize(670,300)
        self.assayt = 2
        self.winfo_toplevel().title("Paddy-PUMP")

        self.ph = tk.Frame(self)
        self.ph2 = tk.Frame(self.ph)
        self.ph_text = tk.Label(self.ph2,text="             Reagent Profile Optimizer",
                                font=self.large_font, fg="#3392ed", anchor='n')
        self.image1 = Image.open(resource_path("Paddy_PUMP.png")).resize((100,100))
        self.image2 = ImageTk.PhotoImage(self.image1)
        self.label1 = tk.Label(self.ph2,image=self.image2)
        self.label1.image = self.image2
        self.label1.pack(side="left",padx=10)
        self.ph_text.pack(side="left",padx=50,fill=BOTH)
        self.ph2.pack(side="top")

        self.text_frame = tk.Frame(self.ph)
        self.text_frame.pack(side="left")
        self.text_label = tk.Label(self.text_frame, text="Status & Directions:", font=self.med_font)
        self.text_label.pack()
        self.text_box = tk.Label(self.text_frame,
                                 text="Select channel and\n enter directory name",
                                 relief=GROOVE)
        self.text_box.pack(padx=5)
        self.fval = tk.StringVar()
        self.fval.set('Channel Valve #')
        self.fmen = tk.OptionMenu(self.ph, self.fval,'Channel 1','Channel 2',
                                  'Channel 3','Channel 4','Channel 5','Channel 6',
                                  'Channel 7','Channel 8','Channel 9')
        self.fmen.pack()
        self.ph.pack(side="left")
        self.entry_and_wkdir_box = tk.Frame(self.ph)
        self.dirtxt = tk.Label(self.entry_and_wkdir_box, text='Dir. Name:')
        self.dirtxt.pack(side='left')
        self.entry_box = tk.Entry(self.entry_and_wkdir_box, width=8)
        self.entry_box.pack(side='left')

        self.wkdir_button = tk.Button(self.entry_and_wkdir_box,
                                   text = 'Create Working Directory',
                                   command = self.make_folder)
        self.wkdir_button.pack(side='right')
        
        self.entry_and_wkdir_box.pack()
        self.button_frame = tk.Frame(self,bg = '#f5f5f5', bd=1, relief="raised",height=24,width=372)
        self.content_frame = tk.Frame(self, width=500, height = 5)

        self.exl_and_recover_box = tk.Frame(self.ph)

        self.exl_but = tk.Button(self.exl_and_recover_box,
                                 text = 'Process MS Data',
                                 command = self.process_file)
        self.exl_but.pack(side="left")
        self.exl_but.configure(state="disabled")

        self.recover_button = tk.Button(self.exl_and_recover_box,
                                     text = 'Recover Pump-Pulse',
                                     command = self.recovery_mode)
        self.recover_button.pack(side="left")

        self.convert_button = tk.Button(self.exl_and_recover_box,
                                        text = 'txt to csv',
                                        command = self.Xcalibur_preprocessing)
        self.convert_button.configure(state="disabled")
        self.convert_button.pack(side="left")


        self.recover_button.pack(side="left")
        self.exl_but.pack(side="left")
        self.exl_and_recover_box.pack()



    def process_file(self):
        """Process CSV file and assign resolution values to paddy.

        Note that the csv_file does not need to be in the working directory.

        """
        csv_file = filedialog.askopenfilename(title='Select CSV for Paddy')#this is a full path
        pp = subprocess.run(["python",resource_path("Iterate.py"),
                             "-x",f"{self.working_dir}","-y",csv_file,"-z",
                             str(self.paddy_iteration),"-v",str(self.fval.get()[-1])])
        self.paddy_iteration += 1
        complete_dumby = open(self.working_dir+"complete_var","r")
        cont_var = complete_dumby.readline()
        complete_dumby.close()
        if cont_var == 'not done':
            print('log file worked')
        else:
            self.text_box['text']="Paddy complete!\nCheck for results."
            self.done_window = tk.Toplevel(self)
            self.done_label = tk.Label(self.done_window, text="\nOptimization complete, check working directory.\n\n\nFile name:'solution_file'\n")
            self.done_label.pack()
        #task function for paddy
        
    def make_folder(self):
        self.make_dir = True
        if self.fval.get()[-1] == '#':
            tk.messagebox.showwarning("Entry Error",
                                      "You need to select the reagent channel",
                                      icon="warning")
            self.make_dir = False
        if self.entry_box.get() == "":
            tk.messagebox.showwarning("Entry Error",
                                      "You need to enter the directory name",
                                      icon="warning")
            self.make_dir = False
        if self.make_dir:
            self.dir_path = filedialog.askdirectory(title='Select folder to save results')
            self.savedir = self.entry_box.get()
            print(self.savedir)
            print(self.dir_path)
            self.working_dir = self.dir_path + '/' + self.savedir + '/'
            os.makedirs(self.working_dir)
            pp = subprocess.run(["python",resource_path("Initiation.py"),"-x",
                                 f"{self.working_dir}","-v",str(self.fval.get()[-1])])
            print('test')
            self.exl_but.configure(state="normal")
            self.convert_button.configure(state="normal")
            self.entry_box.configure(state="disabled")
            self.fmen.configure(state="disabled")
            self.wkdir_button.configure(state="disabled")
            #self.lbut.configure(state="disabled")
            print(self.working_dir)
            self.text_box['text']="Run HPLC-MS experiment\nwith recipe\n and process export file"
            self.paddy_iteration = 0

    def recovery_mode(self):
        #select directory with paddy_runner instance
        #makes the state ready for csv processing by getting the working dir path
        #and iteration by selecting the pickle file (and subsequently the dir)
        #not absolutely bug proof, so some understanding is needed sense it can go off the rails
        #this function anticipates that one will be fine with writing to the directory
        self.recover_bool = True
        if self.fval.get()[-1] == '#':
            tk.messagebox.showwarning("Entry Error",
                                      "You need to select the reagent channel",icon="warning")
            self.recover_bool = False
        if self.recover_bool:
            self.pickle_path = filedialog.askopenfilename(title="Select Paddy (pickle) file",
                                                          filetypes=[("pickle",".pickle")])
                                                          #only allows selection of pickles
            print(self.pickle_path)
            temp = self.pickle_path.split(".")[-2].split("_")
            print(temp)
            temp2 = ""
            if temp[-1] != "backup":
                self.paddy_iteration = int(self.pickle_path.split(".")[-2].split("_")[-1])#
                self.working_dir = self.pickle_path.split(f"iteration_{self.paddy_iteration}")[0]
            else:
                self.paddy_iteration = int(temp[-2])
                self.working_dir = self.pickle_path.split(f"iteration_{self.paddy_iteration}_")[0]
            #note that the above is not bug proof
            if self.working_dir != None:
                self.exl_but.configure(state="normal")
                self.convert_button.configure(state="normal")
                self.entry_box.configure(state="disabled")
                self.fmen.configure(state="disabled")
                self.wkdir_button.configure(state="disabled")
                self.text_box['text']="Run HPLC-MS experiment\nwith recipe\n and process export file"
                complete_dumby = open(self.working_dir+'complete_var','w+')
                complete_dumby.write('not done')
                complete_dumby.close()

    def Xcalibur_preprocessing(self):
        #this function makes a csv file from an exported .txt chromatogram
        txt_file = filedialog.askopenfilename(title="Select .txt file",
                                              filetypes=[("txt",".txt")])
        temp = txt_file.split("/")
        if len(temp[-1].split(".")) > 1:#if theres a file extension
            csv_file = temp[-1].split(".")[0]+".csv"
        else:
            csv_file = temp[-1]+".csv"
        with open(txt_file,"r") as f:
            file_length = len(f.readlines())
        csv_source = open(txt_file,"r")
        print(self.working_dir+csv_file)
        csv_dest = open(self.working_dir+csv_file,'w+')
        for i in range(file_length):
            line = csv_source.readline()
            if len(line.split("\t")) == 1:
                csv_dest.write(line)
            else:
                csv_dest.write(line.split("\t")[0]+","+line.split("\t")[1])
        csv_dest.close()

if __name__ == "__main__":
    app =  Wizard()
    app.mainloop()

