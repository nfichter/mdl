import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
	"""
	This function runs an mdl script
	"""
	color = [255, 255, 255]
	tmp = new_matrix()
	ident( tmp )

	p = mdl.parseFile(filename)

	if p:
		(commands, symbols) = p
	else:
		print "Parsing failed."
		return

	ident(tmp)
	stack = [ [x[:] for x in tmp] ]
	screen = new_screen()
	tmp = []
	step = 0.1
	for command in commands:
		line = command[0]
		args = [x for x in command]
		del args[0]
		
		if line == '':
			pass

		#PUSH/POP
		elif line == 'push':
			stack.append([row[:] for row in stack[len(stack)-1]])
		elif line == 'pop':
			stack.pop()
			
		#SCALE/MOVE/ROTATE
		elif line == 'scale':
			t = make_scale(float(args[0]), float(args[1]), float(args[2]))
			matrix_mult(stack[len(stack)-1],t)
			stack[len(stack)-1] = t
		elif line == 'move':
			t = make_translate(float(args[0]), float(args[1]), float(args[2]))
			matrix_mult(stack[len(stack)-1],t)
			stack[len(stack)-1] = t
		elif line == 'rotate':
			theta = float(args[1]) * (math.pi / 180)
			if args[0] == 'x':
				t = make_rotX(theta)
			elif args[0] == 'y':
				t = make_rotY(theta)
			else:
				t = make_rotZ(theta)
			matrix_mult(stack[len(stack)-1],t)
			stack[len(stack)-1] = t
		
		#BOX/SPHERE/TORUS
		elif line == 'box':
			temp = []
			add_box(temp,
					float(args[0]), float(args[1]), float(args[2]),
					float(args[3]), float(args[4]), float(args[5]))
			matrix_mult(stack[len(stack)-1], temp)
			draw_polygons(temp, screen, color)
		elif line == 'sphere':
			temp = []
			add_sphere(temp,
					   float(args[0]), float(args[1]), float(args[2]),
					   float(args[3]), step)
			matrix_mult(stack[len(stack)-1], temp)
			draw_polygons(temp, screen, color)
		elif line == 'torus':
			temp = []
			add_torus(temp,
					  float(args[0]), float(args[1]), float(args[2]),
					  float(args[3]), float(args[4]), step)
			matrix_mult(stack[len(stack)-1], temp)
			draw_polygons(temp, screen, color)
		
		#LINE
		elif line == 'line':
			temp = []
			add_edge( temp,
					  float(args[0]), float(args[1]), float(args[2]),
					  float(args[3]), float(args[4]), float(args[5]) )
			draw_lines(temp, screen, color)
			
		#SAVE/DISPLAY
		elif line == 'display' or line == 'save':
			if line == 'display':
				display(screen)
			else:
				save_extension(screen, args[0])