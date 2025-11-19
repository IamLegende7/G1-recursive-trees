import math

debug = True
file = 'image.svg'

## SETTINGS ##
# General
mode = "line"

# Board
height = 900
width = 1600

# Size
initial_size = 200
dropoff = 1.38
line_width = 1/20
exponential_dropoff = True

# Generations & Children
max_generations = 10
children_count = 2

## SVG STUFF ##
def init_file(filename):
  open(filename, 'w').close()
  to_file(f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="{str(width)}" height="{str(height)}">')
  to_file(f'<rect width="{str(width)}" height="{str(height)}" fill="#FFFFFF" />')

def to_file(contents: str):
    try: 
      with open(file, 'a') as f: f.write(contents + "\n")
    except: 
      print("Error writing to svg file!")

def draw_line(x1: float, y1: float, x2: float, y2: float, width: float, colour: str = "#000000"):
    line_str = f'<line x1="{str(x1)}" y1="{str(y1)}" x2="{str(x2)}" y2="{str(y2)}" stroke="{colour}" stroke-width="{str(width)}" />'
    to_file(line_str)

## NODES ##
def node(startx, starty, generation, alpha, length):
  
  if exponential_dropoff: new_length = length / dropoff
  else: new_length = initial_size / (generation * dropoff + 1)
  x_offset = math.sin(alpha * (math.pi / 180)) * new_length
  y_offset = math.cos(alpha * (math.pi / 180)) * new_length

  ## Mathe

  dist = 180 / children_count

  if debug: print(f"Gen: {generation} Dist: {dist}")

  endx = startx + x_offset
  endy = starty + y_offset

  ## Drawing
  if mode == "line":
    draw_line(x1=startx, y1=starty, x2=endx, y2=endy, width=(new_length * line_width), colour="#000000")

  if generation > max_generations: return

  ## Generate Children
  for i in range(children_count):
    cur_rot = (i+0.5) * dist + alpha - 90
    node(endx, endy, generation+1, cur_rot, new_length)


## INIT ##
init_file(file)

## GENERATING TREE ##
node((width / 2), 0, 0, 0, initial_size*2)

## CLEANUP ##
to_file('</svg>')
print("done stuff")