# -*- coding: utf-8 -*-
"""
@author: Hugo
"""
from InputFile import InputFile
from Slice import Slice
from OutputFile import OutputFile
from random import shuffle
from itertools import product

class Pizza:         
    
    def __init__(self,rows,cols,min_ham,max_cells,matrix):
        self.rows=rows
        self.columns=cols
        self.hams=min_ham
        self.maxCells=max_cells
        self.ingredients=matrix
        self.expanders=[]
        self.occupied={}
                
    def list_expanders(self,sort=True,reverse=True):
        """ 
        A slice must have at least W number of cells, and a maximum of S cells,
        with W being the minimum number of hams and S the maximum number of cells in a slice.
        This function generates a list with possible heights and widths combinations that, 
        when added to the coordinates of a cell, create slices within the limits. According
        with the parameters, the result can be a sorted list, either in ascending or
        descending order, or a randomly shuffled list
        
        :return: list of possible expanders to form a slice
        """
        
        #The expander is a tuple with two values to be added to, respectively, the row and the column of a given position, in order to form a slice
        expanders=[]            
        for x in range(self.maxCells):
            for y in range(self.maxCells):
                area=(x+1)*(y+1)
                if self.hams<=area<=self.maxCells:          #The minimal possible area for a slice is the minimum number of hams
                    expanders.append((x,y))
                    
        def sort_by_area(xy):
            x,y=xy
            return(x+1)*(y+1)
        if sort:
            return sorted(expanders,key=sort_by_area,reverse=reverse)
        else:
            shuffle(expanders)
            return expanders
    
    def generate_occupied(self):
        """
        This function generates a dictionary with a boolean for each cell indicating
        whether it is already part of a cutted slice or not. The dictionary is created
        using shuffle to make it random when it's generated multiple times.
        
        :return: dictionary of tuples with boolean values for cells included in slices or not
        """
        
        #This dictionary contains the information on whether a cell has been already included in a previous slice or not
        #It starts with the all the cells as keys and all the values set to False
        keys=[]
        for x in range(self.rows):
            for y in range(self.columns):
                keys.append((x,y))
        shuffle(keys)
        values = [False] * len(keys)
        return dict(zip(keys, values))
        
    def cut_slice(self):
        """
        This method randomly (due to the shuffle in the dictionary creation) searches for a 
        cell, then uses an expander as guidance to define a slice and cuts it, if all the 
        requirements are met. If not, it will search until one is found.
        
        :return: Slice object with the coordinates of the slice
        """
        
        #Iterates on the dictionary of cells to search for an unoccupied (or uncutted) cell
        for (r1,c1),is_occupied in self.occupied.items():
            if not is_occupied:
                for height,width in self.expanders:     #Iterates on the list of expanders
                    overlap=False                       #Flag to signal if there's overlap between the slice created and a previous one
                    hams=0                              #Variable to store the number of hams in a slice
                    if (r1+height)<self.rows and (c1+width)<self.columns:           #Check if the slice is within boundaries of the pizza
                        sliceIdxs = list(product(range(r1, r1 + height + 1), range(c1, c1 + width + 1)))
                        for x,y in sliceIdxs:
                            if self.occupied[(x,y)]:
                                overlap=True
                                break                   #Exit the search if one occupied cell is found in the slice
                            if self.ingredients[x][y]=="H":
                                hams+=1
                        if not overlap and hams>=self.hams:     #Check if the slice meets the requirements (minimum number of hams and no overlap - maximum number of cells per slice is assured by self.expanders)
                            for x,y in sliceIdxs:
                                self.occupied[(x,y)]=True       #Occupy the cells in the slice
                            return Slice(r1,c1,r1+height,c1+width)      #Return a Slice object

        return
                
    def sub_sample_slicer(self,factor=10):
        """
        This function creates the slices for the sub-sample that serves as comparer.
        The number of slices used to the comparison is set to 1/[factor] of the number of slices
        with maximum size (maxCells) possible in the pizza, defined as the area of the pizza
        over the number of maxCells in a slice.
        
        :return: list of slices made, the score for the sum of the slices and a dictionary with 
        all the cells included
        """
        
        #This method creates a sub-sample with an exact number of slices calculated in nSlices.
        nSlices=int(round(((self.rows*self.columns)/self.maxCells)/factor))  #Number of slices to cut, using a factor given as a parameter
        cumScore=0                       #Acumulated score of the slices (sum of the areas of the slices)
        setSlices=[]                     #List containing the coordinates of all the slices cutted  
        self.occupied=self.generate_occupied()      #Setting all the cells as unoccupied for each sub-sample created
        for x in range(nSlices):            
            s=self.cut_slice()          #Cut a new slice
            if s:
                cumScore+=s.score()     #Add the area/score of the slice to the cumulative Score
                setSlices.append(s)     #Append the slice to the list of slices
        occupied=self.occupied.copy()   #Save the current state of the occupied dictionary
        return setSlices,cumScore,occupied          #Return the list of slices, its score and dictionary of occupied cells
    
    def sub_samplers_iterator(self,sample_threshold=20,factor=10,sort=True,reverse=True):
        """
        This function iterates on sub-sample slicers, in order to compare them and keep the best one.
        The iteration stops after [sample_threshold] iterations in a row that don't increase the score.
        
        :return: list of slices with best score, the score and a dictionary with the cells occupied by
        the returned set of slices
        """
        
        self.expanders=self.list_expanders(sort=sort,reverse=reverse)       #Generate list of expanders with given sort and reverse parameters
        bestScore=0             #Keep the best score
        bestSet=[]              #Keep the best set of slices
        currentOccupied={}      #Keep the current dictionary of occupied cells
        noIncrease=0            #Variable to count the number of times a sub-sample is created without increasing the best score
        while noIncrease<sample_threshold:         #While the score doesn't stop increasing for [sample_threshold] times in a row:
            setSlices,score,occupied=self.sub_sample_slicer(factor)         #Generate a new sub-sample from sub_sample_slicer with given factor
            if score > bestScore:           #If the new score is higher than the current best score:
                bestScore=score             #Best score assumes the new score
                bestSet=setSlices           #Best set of slices assumes the new set of slices
                currentOccupied=occupied    #Current occupied assumes the new dictionary of occupied cells
                noIncrease=0                #Count restarts
            else:
                noIncrease+=1               #1 added to the count
        return bestSet,bestScore,currentOccupied        #Return the best set of slices,its score and the dictionary of occupied cells
    
    def final_slicer(self,threshold=30,sample_threshold=20,factor=10,sampling_sort=True,slicer_sort=True,sampling_reverse=True,slicer_reverse=True):
        """
        This method cuts the rest of the pizza, starting with the best sub-sampler selected
        in the previous methods. Then, it will iterate [threshold] times on the cutting of
        the rest of the pizza and save the one with the best score.
        
        :return: list of final slices
        """
        
        #This method takes the best sub-sample selected in sub_samplers_iterator, and starts cutting the resting of the pizza from this point
        slices,score,occupied=self.sub_samplers_iterator(sample_threshold,factor,sampling_sort,sampling_reverse)    #Saves the returns from the sub-sample iterator in variables
        bestScore=score     #The first best score is the score from the sub-sample
        bestSet=slices      #The first best set of slices is the one from the sub-sample
        self.expanders=self.list_expanders(sort=slicer_sort,reverse=slicer_reverse)     #Creates a new list of expanders with given sort and reverse values (so it can differ from the ones used in sub-sampling)
        noIncrease=0        #Variable to count the number of times a pizza is cutted without increasing the best score
        while noIncrease < threshold:     #While the number of iterations is lower than the given threshold:
            cumScore=score          #Cumulative score starts with the score from the sub-sample
            setSlices=slices        #Initial set of slices is the one from the sub-sample
            self.occupied=occupied      #The dictionary of occupied cells is the one inherited from the sub-sample
            complete=False          #Flag to check whether the pizza cutting is complete or not
            while not complete:     #While there's pizza to cut:
                s=self.cut_slice()      #Cut a slice
                if s:               #If there's a slice cutted:
                    cumScore+=s.score()     #Add the slice's score to the cumulative score
                    setSlices.append(s)     #Append the slice to the set of slices
                else:
                    complete=True   #If no slice is returned, cutting of the pizza is completed
            if cumScore>bestScore:      #If the cumulative score is higher than the best score stored:
                bestScore=cumScore      #Set this score as the best score
                bestSet=setSlices       #Set the set of slices as the best one
                noIncrease=0            #Count restarts
            else:
                noIncrease+=1           #1 added to the count
        return bestSet              #Return the best set of slices
        
if __name__ == "__main__":
    pizza_file = InputFile("input_7.txt")
    pizza_file.read()
    rows,cols,ham,cells,matrix=pizza_file.to_pizza()
    p=Pizza(rows,cols,ham,cells,matrix)
    slicesList=p.final_slicer(threshold=30,
                              sample_threshold=20,
                              factor=10,
                              sampling_sort=True,
                              slicer_sort=True,
                              sampling_reverse=True,
                              slicer_reverse=True)
    o=OutputFile(slicesList,"output_7.txt")
    o.write()
    
