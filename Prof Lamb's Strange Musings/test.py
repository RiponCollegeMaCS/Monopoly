%cython
# Timer code.
import time
timeList = []


def timer():
    timeList.append(time.time())
    if len(timeList) % 2 == 0:
        print('Time elapsed: ' + str(round(timeList[-1] - timeList[-2], 4)) + ' seconds.')
        timeList.pop()
        timeList.pop()



def is2pow(n):
    while n != 0 and n%2 == 0:
        n = n >> 1
    return n == 1

timer()
results_list = []
for i in range(1000):
    results_list.append(is2pow(i))
print(results_list.count(True))
timer()