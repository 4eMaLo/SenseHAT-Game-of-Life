import sense_hat
from time import sleep

disp = sense_hat.LedMatrix()
dpad = sense_hat.DPad()
disp.clear()

FIELD_SIZE_X = 128
FIELD_SIZE_Y = 128
COLOR = (0,6,48)


matrix =          [[0 for y in range(FIELD_SIZE_Y)] for x in range(FIELD_SIZE_X)]
matrix_next_gen = [[0 for y in range(FIELD_SIZE_Y)] for x in range(FIELD_SIZE_X)]

'''
# --- Glider ----
matrix[2][2] = 1
matrix[1][3] = 1
matrix[0][1] = 1
matrix[0][2] = 1
matrix[0][3] = 1
# --------------
'''

# --- Initial Pattern
matrix[1][2] = 1
matrix[1][3] = 1
matrix[2][1] = 1
matrix[2][2] = 1
matrix[3][2] = 1
# ---------------

VIEWPORT_X = 0
VIEWPORT_Y = 0


SIMULATION = False


def neighbour_count(matrix, x,y):
	''' Count the number of neighbours for the specified cell '''
	count = 0
	for i,j in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
		if matrix[(x+i)%FIELD_SIZE_Y][(y+j)%FIELD_SIZE_Y] > 0:
			count += 1
	return count

trigger_m, lock_m = False, False
trigger_u, lock_u = False, False
trigger_d, lock_d = False, False
trigger_l, lock_l = False, False
trigger_r, lock_r = False, False

while 1:
	joy = dpad.get_state()
	mid_click = joy[4]
	if mid_click and not trigger_m and not lock_m:
		lock_m = True
	if not mid_click and not trigger_m and lock_m:
		trigger_m = True
		lock_m = False
	if mid_click and trigger_m and not lock_m:
		lock_m = True
	if not mid_click and trigger_m and lock_m:
		trigger_m = False
		lock_m = False


	left = joy[2]
	if left and not trigger_l and not lock_l:
		trigger_l = True
		lock_l = True
	elif trigger_l and lock_l:
		trigger_l = False
	if not left and lock_l:
		lock_l = False

	right = joy[3]
	if right and not trigger_r and not lock_r:
		trigger_r = True
		lock_r = True
	elif trigger_r and lock_r:
		trigger_r = False
	if not right and lock_r:
		lock_r = False

	up = joy[0]
	if up and not trigger_u and not lock_u:
		trigger_u = True
		lock_u = True
	elif trigger_u and lock_u:
		trigger_u = False
	if not up and lock_u:
		lock_u = False

	down = joy[1]
	if down and not trigger_d and not lock_d:
		trigger_d = True
		lock_d = True
	elif trigger_d and lock_d:
		trigger_d = False
	if not down and lock_d:
		lock_d = False

	if trigger_l:
		VIEWPORT_Y -= 1
		VIEWPORT_Y %= FIELD_SIZE_Y

	if trigger_r:
		VIEWPORT_Y += 1
		VIEWPORT_Y %= FIELD_SIZE_Y

	if trigger_u:
		VIEWPORT_X -= 1
		VIEWPORT_X %= FIELD_SIZE_X

	if trigger_d:
		VIEWPORT_X += 1
		VIEWPORT_X %= FIELD_SIZE_X

	SIMULATION = trigger_m



	for x in range(8):
		for y in range(8):
			val = matrix[(x+VIEWPORT_X)%FIELD_SIZE_X][(y+VIEWPORT_Y)%FIELD_SIZE_Y]
			if val == 1:
				disp.set_pixel_fb(x,y, COLOR)
			elif val == 0:
				disp.set_pixel_fb(x,y, (0,0,0))
	disp.fb_flush()

	if SIMULATION:
		for x in range(FIELD_SIZE_X):
			for y in range(FIELD_SIZE_Y):
				n = neighbour_count(matrix, x, y)

				if n == 3: # Born cell
					matrix_next_gen[x][y] = 1
				elif n < 2 or n > 3: # Dying cell
					matrix_next_gen[x][y] = 0
				else:
					matrix_next_gen[x][y] = matrix[x][y]


		for x in range(FIELD_SIZE_X):
			for y in range(FIELD_SIZE_Y):
				matrix[x][y] = matrix_next_gen[x][y]
