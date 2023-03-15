import tkinter as tk
from tkinter import filedialog
import Model
import os
import threading



class ViewController():

   buttonHeight = 1
   buttonWidth = 20

   def __init__(self):
      pass
      

   def run(self):
      window = tk.Tk()
     
      window.title("Starling File Converter")

      self.outputLabel = tk.Label(text="", justify="left")

      self.model =  Model.Model(self.outputLabel)

      self.browseButton = tk.Button(text="Browse for Starling File",
                           command=self.browseButtonWasClicked, width=self.buttonWidth, height=self.buttonHeight)
      self.convertButton = tk.Button(text="Convert to Manager.io file", command=self.convertButtonWasClicked,
                           state='disabled', width=self.buttonWidth, height=self.buttonHeight)
      
      self.browseButton.pack()
      self.convertButton.pack()
      self.outputLabel.pack()
      window.geometry("400x500")

      window.mainloop()


   def browseForFile(self):
        file = filedialog.askopenfile(
            mode='r', filetypes=[('Starling Files', '*.csv')])
        return file


   def browseButtonWasClicked(self):
      model = self.model
      model.initialise()
      model.sourceFile = self.browseForFile()
      model.sourcePath = os.path.normpath(model.sourceFile.name)
      pathList = model.sourcePath.split(os.sep)
      self.outputLabel["text"] = pathList[-1] + " read"
      model.fileReadingConversionAndWritingProcess()
      self.convertButton['state'] = "normal"


   def convertButtonWasClicked(self):
      self.convertButton['state'] = "disabled"
      backgroundThread = threading.Thread(target=self.model.convert(), args=(1,))
      backgroundThread.start




   
      
