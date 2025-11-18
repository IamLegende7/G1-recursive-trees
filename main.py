from svg import SVGWriter
import math

debug = False

## SETTINGS ##
# Board
height = 1000
width = 1000

# Size
initial_size = 200
dropoff = 0.5

# Generations & Children
max_generations = 5
initial_children_count = 2
line_width = 4

# Spread
spread = 90
spread_dropoff = 1
do_spread_dropoff = False
keep_rotation = False



# Init
svg_writer = SVGWriter('image.svg')
svg_writer.write(svg_writer.rect(width, height, "#FFFFFF"))

def node(startx: float, starty: float, generation: int, child_num: int, children_count_parent: int, rotation = None):
  
  ## Mathe
  child_multi = child_num - math.ceil(children_count_parent / 2)
  if ((children_count_parent % 2) == 0):
    if child_num <= (children_count_parent / 2): child_multi -= 1
    if child_multi < 0: child_multi += 0.5
    else: child_multi -= 0.5

  if generation == 0:
    alpha = 0
  else:
    if do_spread_dropoff: spread_full = (spread / (generation / (1 / spread_dropoff)))
    else:                 spread_full = spread

    if (rotation is None) or (not keep_rotation):
      alpha = (            spread_full * child_multi)
    else:
      alpha = (rotation + (spread_full * child_multi))

  alpha_rad = alpha * (math.pi / 180)

  if debug: print(f"Gen: {generation} Alpha: {alpha}")

  x_offset = math.sin(alpha_rad) * (initial_size / (dropoff * (generation + 1)))
  y_offset = math.cos(alpha_rad) * (initial_size / (dropoff * (generation + 1)))

  endx = startx + x_offset
  endy = starty + y_offset


  ## Drawing
  svg_writer.write(svg_writer.line(startx, starty, endx, endy, (line_width / (generation + 1)), "#000000"))

  if generation < max_generations:
    ## Get child count
    if generation == 0:
      children_count = initial_children_count
    else:
      children_count = children_count_parent

    ## Generate Children
    for i in range(children_count):
      node(endx, endy, generation+1, i+1, children_count, rotation=alpha)

# Generating Tree
node(startx=(width / 2), starty=0, generation=0, child_num=1, children_count_parent=1)

# Cleanup
svg_writer.close()