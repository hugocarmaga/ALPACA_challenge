# -*- coding: utf-8 -*-
"""
@author: Hugo
"""

class Slice:
    
    def __init__(self,r1,c1,r2,c2):     #Construct a Slice object with the 4 coordinates needed to identify a slice
        self.r1=r1
        self.r2=r2
        self.c1=c1
        self.c2=c2
        
    def score(self):
        return (abs(self.r2-self.r1)+1)*(abs(self.c2-self.c1)+1)    #Calculate and return the score of the slice
    
    def to_output(self):
        return str(self.r1)+" "+str(self.c1)+" "+str(self.r2)+" "+str(self.c2)      #Method to write the slice in the output format
