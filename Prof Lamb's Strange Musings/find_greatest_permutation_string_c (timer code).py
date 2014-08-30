from __future__ import print_function

#Timer function
import time
timeList = []
"""Print the time elapsed between the first
    and second time this function is called."""
def timer():
    timeList.append(time.time())
    if len(timeList)%2 == 0:
        print('Time elapsed: ' + str(round(timeList[-1] - timeList[-2],4)) + ' seconds.')
        timeList.pop()
        timeList.pop()

#Start timer
timer()

#Put each word in the dictionary file into an array with 28 rows.
#For each 0<i<29, the ith row contains all words of length i.
#The characters in each word are also sorted in ascending alphabetical order.
d_file = open("dictionary.txt", 'r')
word_array = [[] for i in range(1,29)]
for line in d_file:
    for word in line.split():
        word_array[len(word)-1].append(''.join(sorted(word.strip())))

#Import the Counter class
from collections import Counter

#For each word length, create a Counter object consisting of the strings
#in the array created above.
#Combine all of the count data into a single Counter object.
combined_counter = Counter()
for row in word_array:
    combined_counter += Counter(row)

#End timer
timer()
input("Press any key to exit. . .")

#Print the strings with the greatest counts.
print("Most common: ", combined_counter.most_common(2))

#Close all files.
d_file.close()

