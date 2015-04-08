#!/usr/bin/env python3

import subprocess
import time

if __name__ == '__main__':
	player = ""#1 100 5 0 0 0 0"#.split(' ')

	start = time.time()

	processes = [subprocess.Popen('./build/monopoly ' + player, shell=True) for i in range(8)]
	exitcodes = [p.wait() for p in processes]

	end = time.time()
	print(end - start)
	# status = subprocess.call((['./build/monopoly'] + player))
	# if status != 0:
	# 	print("Something went wrong. Status" + status)