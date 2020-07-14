# GUI builder for .its anonymizer app
# Created by: Sarah MacEwan
# Last Updated: August 21, 2019

# TODO:
    # Description of rationale behind each data point being anonymized, and behind what data is being left in (in the README).

import sys
import os

if sys.version_info[0] == 2:
    import Tkinter as tk
    import tkFileDialog
    from tkMessageBox import showwarning, askyesno, showinfo, showerror
else:
    import tkinter as tk
    from tkinter import PhotoImage 
    from tkinter import filedialog as tkFileDialog
    from tkinter.messagebox import showwarning, askyesno, showinfo, showerror
    
import webbrowser
import its_anonymizer
import json

#chrome_path = 'C:\Program Files (x86)\Google\Chrome\Application/chrome.exe %s'


class Anonymizer(object):
    
    def __init__(self, master):
        self.root = master
        self.root.resizable(width=True, height=True)
        self.root.title('ITS Anonymizer')
        self.root.protocol('WM_DELETE_WINDOW')# add function to register pressing the x button as event and call the corresponding function

        program_path = os.getcwd()
        self.frame = tk.Frame(root)
        self.frame.grid(row=0, column=0, sticky='wns', padx=(30, 30), pady=30)
        
        # Instance variables
        self.input_dir = None
        self.output_dir = None
        self.repFile = None # for now, just use the hard-coded replacements dict :)
        self.repFileFullName = 'replacements_dict.json'
        #self.repFileFull = open(self.repFileFullName)
        #self.repDict = json.load(self.repFileFull)
        
        self.checkbuttonVals = []
        self.primaryChildVar= tk.IntVar()
        self.itsVar= tk.IntVar()
        self.childInfoVar= tk.IntVar()
        self.SRDIVar= tk.IntVar()
        self.childVar = tk.IntVar()
        self.timesVar = tk.IntVar()

        # Menu window
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.submenu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='Menu', menu=self.submenu)
        #self.submenu.add_command(label = 'run standard anonymization...', command=self.anonymize_its_files_full)
        readme_link = 'https://github.com/BLLManitoba/ITS_anonymizer/blob/master/README.md'
        self.submenu.add_command(label='Help', command=lambda: webbrowser.open_new(readme_link)) # .get(chrome_path).open_new(readme_link))

        # Input/Output Selection Buttons
        self.input_dir_button = tk.Button(
            self.frame,
            text = 'Select input folder',
            font = ("Times New Roman", 15), 
            command = self.select_input_its,
            height = 1,
            width = 20,
            relief=tk.GROOVE).grid(row=0, column=1, padx=20, pady=5, sticky='W')

        self.output_dir_button = tk.Button(
            self.frame,
            text = 'Select output folder',
            font = ("Times New Roman", 15), 
            command = self.select_output_dir,
            height = 1,
            width = 20,
            relief = tk.GROOVE).grid(row = 1, column = 1, padx=20, pady=5, sticky='W')

        tk.Label(self.frame, text = "Partial anonymization: Select which information you want anonymized",
            font = ("Times New Roman", 15)).grid(row=0, column=0, padx=5, pady=5, sticky='NW')
        
        self.primary_child_checkbox = tk.Checkbutton(
            self.frame,
            text = 'Child Data: date of birth, enrollment date, child ID',
            font = ("Times New Roman", 15), 
            variable = self.primaryChildVar).grid(row=1, column = 0, padx=5, pady=5, sticky='NW')
#        self.its_checkbox = tk.Checkbutton(
#            self.frame,
#            text = 'ITS row',
#            variable = self.itsVar).grid(row=2, column = 0, padx=5, pady=5, sticky='NW')
#        self.child_info_checkbox = tk.Checkbutton(
#            self.frame,
#            text = 'ChildInfo row',
#            variable = self.childInfoVar).grid(row=3, column = 0, padx=5, pady=5, sticky='NW')
#        self.srdi_info_checkbox = tk.Checkbutton(
#            self.frame,
#            text = 'SRD info row',
#            variable = self.SRDIVar).grid(row=4, column = 0, padx=5, pady=5, sticky='NW')
#        self.child_checkbox = tk.Checkbutton(
#            self.frame,
#            text = 'Child row',
#            variable = self.childVar).grid(row=5, column = 0, padx=5, pady=5, sticky='NW')
        self.datetime_checkbox = tk.Checkbutton(
            self.frame,
            text = 'Time Data: file name, time file was created, timestamps',
            font = ("Times New Roman", 15), 
            variable = self.timesVar).grid(row=2, column = 0, padx=5, pady=5, sticky='NW')
            
        # Main (full) anonymizer button
        self.full_anon_button = tk.Button(
            self.frame,
            text = 'Fully anonymize files',
            font = ("Times New Roman", 15), 
            command = self.anonymize_its_files_full,
            height = 1,
            width = 20,
            relief = tk.GROOVE).grid(row = 2, column = 1, padx=5, pady=5)
        
        # Selective anonymizer button
        self.anon_button = tk.Button(
            self.frame,
            text = 'Partially anonymize files',
            font = ("Times New Roman", 15), 
            command = self.anonymize_its_files,
            height = 1,
            width = 20,
            relief = tk.GROOVE).grid(row = 3, column = 0, padx=5, pady=5, sticky='NW')
    
    def get_selection_values(self):
        self.checkbuttonVals = []
        self.checkbuttonVals.append([['PrimaryChild', 'ChildInfo', 'Child'], self.primaryChildVar.get()])
        #self.checkbuttonVals.append([['ITS'], self.itsVar.get()])
        #self.checkbuttonVals.append([['ChildInfo'], self.childInfoVar.get()])
        #self.checkbuttonVals.append([['SRDInfo'], self.SRDIVar.get()])
        #self.checkbuttonVals.append([['Child'], self.childVar.get()])
        self.checkbuttonVals.append([['ITS', 'TransferTime', 'Bar', 'BarSummary', 'Recording', 'FiveMinuteSection', 'Item'], self.timesVar.get()])
        print self.checkbuttonVals
        return self.checkbuttonVals
    
    def select_input_its(self):
        print('selecting inputs...')
        self.input_dir = tkFileDialog.askdirectory()
        
    def select_output_dir(self):
        print('selecting output dir...')
        self.output_dir = tkFileDialog.askdirectory(title='Select where to save your output files')
        
    def anonymize_its_files_full(self):
        print('input is', self.input_dir)
        print('output is', self.output_dir)
        if self.input_dir == None:
            showwarning('Input folder', 'Please select an input folder')
            return
        if self.output_dir == None:
            showwarning('Output folder', 'Please select an output folder')
            return
        print("Fully anonymizing your its files...")
        its_anonymizer.main(self.input_dir, self.output_dir, self.repFileFullName)
        
    def create_partial_file(self):
        print('making a partial replacements dictionary, based on what was selected...')
        with open(self.repFileFullName) as repFileFull:
            self.repDict = json.load(repFileFull)
            print('initial repDict: ', self.repDict)
            for node in self.repDict.keys():
            #print node
                for item in self.get_selection_values():
                    cbVal = item[1]
                    for selectName in item[0]:
                    #print "item name is: ", selectName
                        if selectName == node:
                        #print('cbVal: ', cbVal)
                            if cbVal == 0:
                            #print('deleting node: ', node)
                                del self.repDict[node]
            #for name, value in self.repDict[node].items():
             #   print(node)
              #  for item in checbuttonVals:
               #     elimVal = self.checkbuttonVals[index]
                #    if elimVal == 
                 #       del self.repDict[node]
            with open('partial_replacements_dict.json', 'w') as repf:
                json.dump(self.repDict, repf)
                print repf
        print "outside with block: repf: ", repf, " repFileFull: ", repFileFull
        
    def anonymize_its_files(self):
        print('input is', self.input_dir)
        print('output is', self.output_dir)
        #print('age checkbox vals are: ', self.get_selection_values())
        checkVals = self.get_selection_values()
        chiSelVal = checkVals[0]
        timeSelVal = checkVals[1]
        numSelected = chiSelVal[1] + timeSelVal[1]
        if self.input_dir == None:
            showwarning('Input folder', 'Please select an input folder')
            return
        if self.output_dir == None:
            showwarning('Output folder', 'Please select an output folder')
            return
        if numSelected == 0:
            showwarning('Partial Anonymization', 'To partially analyze a file, at least one checkbox MUST be selected')
            return
        print("anonymizing desired sections of its files...")
        self.create_partial_file()
        its_anonymizer.main(self.input_dir, self.output_dir, 'partial_replacements_dict.json')
        
        os.remove('partial_replacements_dict.json')


if __name__ == '__main__':
    root = tk.Tk()
    x = Anonymizer(root)
    root.mainloop()