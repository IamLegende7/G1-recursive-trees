import math



file = 'image.svg'

# Board
height = 900
width = 1600

# Size
initial_size = 200
dropoff = 1.38

# Generations & Children
max_generations = 7
children_count = 2

## SVG STUFF ##
def to_file(contents: str):
    try: 
      with open(file, 'a') as f: f.write(contents + "\n")
    except: 
      print("Error writing to svg file!")

def init_file(filename):
  open(filename, 'w').close()
  to_file(f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="{str(width)}" height="{str(height)}">')
  to_file(f'<rect width="{str(width)}" height="{str(height)}" fill="#FFFFFF" />')

def draw_line(x1: float, y1: float, x2: float, y2: float, width: float, color: str = "#000000"):
    line_str = f'<line x1="{str(x1)}" y1="{str(y1)}" x2="{str(x2)}" y2="{str(y2)}" stroke="{color}" stroke-width="{str(width)}" />'
    to_file(line_str)

## NODES ##
def node(startx, starty, generation, alpha, length):
  
  new_length = length / dropoff
  
  ## Mathe
  endx = startx + math.sin(alpha * (math.pi / 180)) * new_length
  endy = starty + math.cos(alpha * (math.pi / 180)) * new_length

  ## Drawing
  draw_line(x1=startx, y1=starty, x2=endx, y2=endy, width=(new_length*0.05), color="#000000")


  dist = 180 / children_count

  if generation < max_generations:
    ## Generate Children
    for i in range(children_count):
      cur_rot = (i+0.5) * dist + alpha - 90
      node(endx, endy, generation+1, cur_rot, new_length)


########################################################################################################################

## INIT ##
init_file(file)

## GENERATING TREE ##
node((width / 2), 0, 0, 0, initial_size*2)

## CLEANUP ##
to_file('</svg>')
print("fertig")