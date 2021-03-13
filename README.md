# ALPACA_challenge

This python program consists of four modules (Pizza.py, Slice.py, InputFile.py and OutputFile.py) and its strategy is divided in two parts:  
- Subsampling: an exact number of slices are cut. The number is calculated as:  
>***(Area of the pizza/Max.area of a slice) ⁄ F***  
with F as a given parameter. Sets with this number of slices are created and their scores are compared. The set with the best score after [sample_threshold] (parameter with a number) iterations in a row without changing the best score is selected.  
- Final iteration: starting from the subsample selected, the rest of the pizza is cutted until the best score is achieved and unchanged for [threshold] (parameter) iterations in a row.  
Both parts involve cutting slices starting in random cells. The way a slice is created from a cell can be adjusted with four sorting parameters, two for each part: [sampling_sort] and [sampling_reverse], and [slicer_sort] and [slicer_reverse] for, respectively, the subsampling and the final iteration parts.
