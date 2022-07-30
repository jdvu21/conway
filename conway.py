# conway.py
# game of life sim from python playground textbook
# https://www.youtube.com/watch?v=E8kUJL04ELA&t=235s

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

def update(frameNum, img, grid, N):
	newGrid = grid.copy()
	for i in range(N):
		for j in range(N): # get the positions of all 8 neighbors
			total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] +
			grid[(i-1)%N, j] + grid[(i+1)%N, j] +
			grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
			grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/255)

			# apply Conways's rules at each postion
			if grid[i, j] == ON:
				if (total < 2) or (total > 3):
					newGrid[i, j] = OFF
			else:
				if total == 3:
					newGrid[i,j] = ON
	# update data
	img.set_data(newGrid)
	grid[:] = newGrid[:] # returning [:]??
	return img,
	print('updated!')

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

	# set grid size
	N = 100
	if args.N and int(args.N) > 8:
		N = int(args.N)

	# set animation update interval
	updateInterval = 50
	if args.interval:
		updateInterval = int(args.interval)

	# declare grid and check for glider flag, randomGrid by default
	grid = np.array([])

	if args.glider:
		grid = np.zeros(N*N).reshape(N, N)
		addGlider(1, 1, grid)
	else:
		grid = randomGrid(N)

	# set up the animation
	print('setting up animation...')
	fig, ax = plt.subplots()
	img = ax.imshow(grid, interpolation='nearest')
	ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ), frames=10, interval=updateInterval, save_count=50)
	anim = ani
	if args.movfile:
		print('movie = %s' % (args.movfile))
		anim.save(args.movfile)#, fps=30, extra_args=['-vcodec', 'libx264'])

	plt.show()

# call main
if __name__ == '__main__':
	main()
