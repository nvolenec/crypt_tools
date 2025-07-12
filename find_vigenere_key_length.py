#!/usr/bin/python3
import matplotlib.pyplot as plt
import numpy as np

# I'm going to plot a nice graph
# grab the ciphertext
filetimetable = open("vigenere_ciphertext_GETGOOD-longer.txt","r")
lines=filetimetable.readlines()
filetimetable.close()

# let's make it all one string
working=""
for line in lines:
    for char in line:
        asc=ord(char)
        if (64 < asc < 91) or ( 96 < asc < 123):
            char=char.upper()
            working+=char

# shift  the ciphertext against itself.
# count up number of matches between
# ciphertext and shifted ciphertext
offsets=[]
data=[]

# this is for lebelling the peaks
threshold=0

# let's only do a small number of shifts, more text, longer keys tested.
# you might want to fiddle with the top value in the range
for offset in range(1,int(len(working)/10)):
    matches=0
    for j in range(len(working)-offset):
        if working[j]==working[j+offset]:
            matches+=1
    threshold+=matches
    data.append(matches)
    offsets.append(offset)
    
# this sets a threshold above which a point is labelled
threshold=int(1.2*threshold/offset)

# lets prep the data for plotting
x=np.array(offsets)
y=np.array(data)
plt.plot(x,y)

# let's label any high points
for i in range(len(offsets)):
    if data[i]>threshold:
        plt.text(offsets[i],data[i],str(i+1))
        
# How frequent are x-axis gridlines?
stepsize=int(offset/10)
plt.xticks(np.arange(0, offset, step=stepsize))
# label axes and title
plt.xlabel('Offsets')
plt.ylabel('Matches')
plt.title('Look for peaks that are multiples of some key length')
plt.grid(b=True, which='major', color='#666666', linestyle='-')
# show the graph
plt.show()
