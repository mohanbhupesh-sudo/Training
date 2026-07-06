# create 1st tuple with values -> (10,20,30), 2nd tuple with values -> (40,50,60) and 3rd tuple with values -> (70,80,90)
# a. Concatenate the 3 tuples and store it in "tubleCombined"
tubleCombined = (10, 20, 30) + (40, 50, 60) + (70, 80, 90)
# Repeat the elements of "tubleCombined" 3 times
tubleCombinedRepeated = tubleCombined * 3
# Access the 3rd element of "tubleCombined"
thirdElement = tubleCombined[2]
# Access the first three elements of "tubleCombined"
firstThreeElements = tubleCombined[:3]
# Access the last three elements of "tubleCombined"
lastThreeElements = tubleCombined[-3:]

# Practice slicing the tuple in different ways and print the results
slice4 = tubleCombined[:]       # This will return the entire tuple
slice5 = tubleCombined[7:]      # This will return the elements from index 7 to the end of the tuple
slice8 = tubleCombined[-3:]     # This will return the last three elements of the tuple
slice10 = tubleCombined[3:]     # This will return the elements from index 3 to the end of the tuple
slice11 = tubleCombined[:-3]     # This will return the elements from the start of the tuple up to but not including the last three elements

