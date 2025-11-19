import math

debug = True
file = 'image.svg'

## SETTINGS ##
# General
mode = "line"

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
colour_background = None #"#FFFFFF"
colour_lines      = "#FFFFFF" #"#000000"

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
  draw_rect(width=svg_width, height=svg_height, colour=colour_background)
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

# Diese Funktion malt ein Rechteck in die SVG Datei
def draw_rect(width: float, height: float,                               # Nötiges Zeugs
              colour: str = None,                                        # Farbe
              x: float = 0, y: float = 0,                                # x, y Position
              border_colour: str = None, border_width: str = None,       # Rand
              rotation: str = 0, rotx: float = None, roty: float = None, # Drehen
              comment: str = None
              ):
  rect_parts = [] # Liste, in der alle Teile des Rechtecks gespeichert werden
  
  ## Drehungs Header ##
  if rotx is None: rotx = x # Wenn nicht gesetzt: setze auf x, bzw. y
  if roty is None: roty = y
  if rotation != 0: rect_parts.append(f'<g transform="rotate({rotation}, {rotx}, {roty})">\n')

  ## Nötiges ##
  rect_parts.append(f'<rect')
  rect_parts.append(f'x="{str(x)}" y="{str(y)}" width="{str(width)}" height="{str(height)}"')

  ## Farbe ##
  if not (colour is None): rect_parts.append(f'fill="{colour}"')
  else: rect_parts.append('fill="none"')

  ## Border ##
  if not (border_colour is None): rect_parts.append(f'stroke="{border_colour}"')
  if not (border_width is None): rect_parts.append(f'stroke-width="{str(border_width)}"')

  ## Rect Ende ##
  rect_parts.append('/>')

  ## Kommentar ##
  if not (comment is None): rect_parts.append(f'<!-- {comment} -->')

  ## Drehung Ende ##
  if rotation != 0: rect_parts.append('\n</g>')

  # Alle in rect_str zusammenfügen
  rect_str = ""
  for x in rect_parts:
    rect_str = rect_str + " " + x

  # In die SVG Datei schreiben
  to_file(rect_str)


## NODES ##
def node(startx, starty, generation, alpha, parent_length):
  ## Mathe
  # Länge dieser Node berechnen
  if exponential_dropoff: node_length = parent_length / dropoff
  else: node_length = initial_size / (generation * dropoff + 1)

  # X & Y offset berechnen
  x_offset = math.sin(alpha * (math.pi / 180)) * node_length
  y_offset = math.cos(alpha * (math.pi / 180)) * node_length

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
node((svg_width / 2), 0, 0, 0, initial_size*2) # Aufrufen der Mothernode

## CLEANUP ##
to_file('\n</svg>') # Schreibt den svg footer in die SVG Datei
print("Fertig!")