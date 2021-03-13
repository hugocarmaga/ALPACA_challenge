# -*- coding: utf-8 -*-
"""
@author: Hugo
"""

class OutputFile:
    
    def __init__(self,setOut,filename):
        self.setOut=setOut
        self.filename=filename
        
    def write(self):
        with open(self.filename,'w') as file:   #Write output file
            file.write(str(len(self.setOut))+"\n")  #Write line with the number of slices
            for each in self.setOut:
                file.write(each.to_output()+"\n")   #Write each slice as a line of the file