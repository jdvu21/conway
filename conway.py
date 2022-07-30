# conway.py
# game of life sim from python playground textbook

# to do: save states
# canons and stuff
# c# implementation? 
# run load calc?
# fullscreen, transparent pretty mode

import sys, argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ON = 255
OFF = 0
vals = [ON, OFF]

def randomGrid(N):
	return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N,N)

def addGlider(i, j, grid):
	glider = np.array([[0,    	0,	255],
					   [255,	0,	255],
					   [0,	  255,	255]])
	grid[i:i+3, j:j+3] = glider
	print("glider created")

def addGosperGun(i, j, grid):
	# gospel of faith = 3
	gosper = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,0,255,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,255,255,0,0,0,0,0,0,255,255,0,0,0,0,0,0,0,0,0,0,0,0,0,255,255,0],
[0,0,0,0,0,0,0,0,0,0,0,255,0,0,0,255,0,0,0,0,255,255,0,0,0,0,0,0,0,0,0,0,0,0,0,255,255,0],
[0,255,255,0,0,0,0,0,0,0,255,0,0,0,0,0,255,0,0,0,255,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,255,255,0,0,0,0,0,0,0,255,0,0,0,255,0,255,255,0,0,0,0,255,0,255,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,255,0,0,0,0,0,255,0,0,0,0,0,0,0,255,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,255,0,0,0,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,255,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
	grid[i:i+11, j:j+38] = gosper
	print("gosper glider gun created")

def update(frameNum, img, grid, N):
	newGrid = grid.copy()
	for i in range(N):
		for j in range(N): # using toroidal boundary conditions...
			total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] +
			grid[(i-1)%N, j] + grid[(i+1)%N, j] +
			grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
			grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/255)

			# ...apply Conways's rules at each postion
			if grid[i, j] == ON:
				if (total < 2) or (total > 3):
					newGrid[i, j] = OFF # death first 
			else:
				if total == 3:
					newGrid[i,j] = ON # then life
	# update data
	img.set_data(newGrid)
	grid[:] = newGrid[:] # returning [:]??
	return img,

# main() function
def main():
	# command line arguments are in sys.argv[1], [2] etc
	# [0] is the script name and can be ignored

	# parse arguments using argparse library
	parser = argparse.ArgumentParser(description="runs Conway's game of life simulation")

	# add arguments
	parser.add_argument('--grid-size', dest='N', required=False)
	parser.add_argument('--mov-file', dest='movfile', required=False)
	parser.add_argument('--interval', dest='interval', required=False)
	parser.add_argument('--glider', action='store_true', required=False)
	parser.add_argument('--gosper', action='store_true', required=False)
	args = parser.parse_args()

	# set grid size (32 is very hand sized, 300 hard to pick out details)
	N = 100
	if args.N and int(args.N) > 8:
		N = int(args.N)

	# set animation update interval in milliseconds 
	# (i.e. 500 is quite slow, but easy to follow)
	updateInterval = 50
	if args.interval:
		updateInterval = int(args.interval)

	# declare grid and check for glider flag, randomGrid by default
	grid = np.array([])

	if args.gosper:
		grid = np.zeros(N*N).reshape(N, N)
		addGosperGun(1, 1, grid)
	elif args.glider:
		grid = np.zeros(N*N).reshape(N, N)
		addGlider(1, 1, grid)
	else:
		grid = randomGrid(N)

	# setup animation, saving it to file first before pyplot can display itself and consume the 
	fig, ax = plt.subplots()
	img = ax.imshow(grid, interpolation='nearest')
	ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ), frames=30, interval=updateInterval, save_count=50)
	anim = ani
	if args.movfile:
		print('saving movfile as %s' % (args.movfile))
		anim.save(args.movfile) # removed extra args - doesnt work for some reason
	print('simulating:')
	plt.show() # simulation is live at this point

# call main
if __name__ == '__main__':
	main()
