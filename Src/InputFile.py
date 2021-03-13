# -*- coding: utf-8 -*-
"""
@author: Hugo
"""

class InputFile:            #Object to read input file
    
    def __init__(self, filename):
        if not filename:
            raise ValueError('File name is not valid')
        self.file = filename
        self.header = []
        self.rows = 0
        self.cols = 0
        self.min_ham = 0
        self.max_cells = 0
        self.matrix = []
        
    def read(self):
        with open(self.file, 'r') as file:          #Open the file
            self.header = file.readline().strip().split(" ")    #Read the first line and assign the values in it to variables
            self.rows = int(self.header[0])
            self.cols = int(self.header[1])
            self.min_ham = int(self.header[2])
            self.max_cells = int(self.header[3])
            for _ in range(self.rows):
                line=file.readline().strip()
                row = [char for char in line]
                self.matrix.append(row)         #Create the matrix with the ingredients
                
    def to_pizza(self):
        return self.rows, self.cols, self.min_ham, self.max_cells, self.matrix      #Return the variables to be used in Pizza()
    
