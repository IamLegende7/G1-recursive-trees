import math

print("DIESE VERSION VON MAIN.PY IST ALT UND NICHT MEHR IN GEBRAUCH!")

debug = False
file = 'image.svg'

## SETTINGS ##
# General
mode = "line"
start = "top"

# Board
svg_height = 900
svg_width = 1600

# Size
initial_size = 200
dropoff = 1.38
exponential_dropoff = True
line_width = 1/20

# Rotation
keep_rotation = True

# Colour
colour_background = None
colour_lines      = "#FFFFFF"

# Generations & Children
max_generations = 10
children_count = 2

## SVG STUFF ##
# Diese Funktion schreibt den SVG header und den Hintergrund in die SVG Datei
def init_file(filename):
  open(filename, 'w').close() # SVG Datei leeren
  to_file('<?xml version="1.0" encoding="UTF-8"?>') # xml header
  to_file(f'<svg xmlns="http://www.w3.org/2000/svg" width="{str(svg_width)}" height="{str(svg_height)}">') # svg header

  # Hintergrund
  to_file(f'<rect width="{str(svg_width)}" height="{str(svg_height)}" fill="{colour_background}" />')
  # Kleiner contents marker; macht die svg Datei weningstents ein bisschen übersichtlicher
  to_file('<!-- vv Contents vv -->\n')

# Diese Funktion schreibt strings in die SVG Datei
def to_file(contents: str):
  try: # Error handling
    with open(file, 'a') as f: # SVG Datei öffnen
      f.write(contents + "\n") # Contents in die SVG Datei schreiben
  except: # (try-except-struktur: wenn die Befehle oben einen Crash produzieren, wird stattdessen der Code hier vv ausgeführt)
    print("Error writing to svg file!")

# Diese Funktion schreibt (bzw. "malt") eine linie in die SVG Datei
def draw_line(x1: float, y1: float, x2: float, y2: float, 
              width: float,
              colour: str = "#000000",
              comment: str = None
              ):
  line_str = f'<line x1="{str(x1)}" y1="{str(y1)}" x2="{str(x2)}" y2="{str(y2)}" stroke="{colour}" stroke-width="{str(width)}" />'
  if not (comment is None): line_str = line_str + f' <!-- {comment} -->'
  to_file(line_str)

## NODES ##
def node(startx, starty, generation, alpha, parent_length):
  ## Mathe
  # Länge dieser Node berechnen
  if exponential_dropoff: node_length = parent_length / dropoff
  else: node_length = initial_size / (generation * dropoff + 1)

  alpha_rad = alpha * (math.pi / 180)

  # X & Y offset berechnen
  x_offset = math.sin(alpha_rad) * node_length
  y_offset = math.cos(alpha_rad) * node_length

  # Optionale Debug Infos
  if debug: print(f"Gen: {generation} Alpha: {alpha}")

  # Berechnen der End-Koordinaten
  endx = startx + x_offset
  endy = starty + y_offset

  ## Drawing
  # Also das malen dieser Node in die SVG Datei
  if mode == "line":
    draw_line(x1=startx, y1=starty, x2=endx, y2=endy,
              width=(node_length * line_width), 
              colour=colour_lines, 
              comment=f"Gen: {generation}")
  elif mode == "quad":
    draw_rect(x=startx, y=(starty - node_length),    # startx|(starty - node_length) = linke, untere ecke
              height=node_length, width=node_length,
              border_colour=colour_lines, border_width=4,
              comment=f"Gen: {generation}"
              )

  ## Generate Children
  if generation < max_generations: # Limitiert die Generationen
    child_spacing = 180 / children_count
    for i in range(children_count): # Wiederholen für alle children, die generiert werden sollen
      child_rotation = (i+0.5) * child_spacing + alpha - 90
      node(endx, endy, generation+1, child_rotation, node_length) # Generiert eine neue Node


#####################
# EIGENTLICHER CODE #
#####################

## INIT ##
init_file(file)

## GENERATING TREE ##
# Aufrufen der Mothernode
if start == "top":
  node((svg_width / 2), 0, 0, 0, initial_size*dropoff)
elif start == "bottom":
  node((svg_width / 2), svg_height, 0, 180, initial_size*dropoff)

## CLEANUP ##
to_file('\n</svg>') # Schreibt den svg footer in die SVG Datei
print("Fertig!")