import math

debug = False
file = 'image.svg'

## SETTINGS ##
# General
mode = "quad"
start = "bottom"

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
spread = 45 # Not working with lines; keep 0 for now!

# Colour
colour_background = "#FFFFFF"
colour_lines      = "#000000"

# Generations & Children
max_generations = 20
children_count = 1
initial_children_count = None

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
              comment: str = None,
              addtional_option: str = None
              ):
  # Grund String
  line_str = f'<line x1="{str(x1)}" y1="{str(y1)}" x2="{str(x2)}" y2="{str(y2)}" stroke="{colour}" stroke-width="{str(width)}"'
  # Extra optionen
  if not (addtional_option is None): line_str = line_str + " " + addtional_option

  # Ende line funktion
  line_str = line_str + ' />'

  # Kommentar
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

  ## Nötiges ##
  rect_parts.append(f'<rect')
  rect_parts.append(f'x="{str(x)}" y="{str(y)}" width="{str(width)}" height="{str(height)}"')

  ## Farbe ##
  if not (colour is None): rect_parts.append(f'fill="{colour}"')
  else: rect_parts.append('fill="none"')

  ## Border ##
  if not (border_colour is None): rect_parts.append(f'stroke="{border_colour}"')
  if not (border_width is None): rect_parts.append(f'stroke-width="{str(border_width)}"')

  ## Drehung ##
  if rotx is None: rotx = x # Wenn nicht gesetzt: setze auf x, bzw. y
  if roty is None: roty = y
  if rotation != 0: rect_parts.append(f'transform="rotate({rotation}, {rotx}, {roty})"')

  ## Rect Ende ##
  rect_parts.append('/>')

  ## Kommentar ##
  if not (comment is None): rect_parts.append(f'<!-- {comment} -->')

  # Alle in rect_str zusammenfügen
  rect_str = ""
  for x in rect_parts:
    rect_str = rect_str + " " + x

  # In die SVG Datei schreiben
  to_file(rect_str)


## NODES ##
def node(P1_x, P1_y, generation, alpha, parent_length):
  ## Mathe
  # Länge dieser Node berechnen
  if exponential_dropoff: node_length = parent_length / dropoff
  else: node_length = initial_size / (generation * dropoff + 1)

  ## BERECHNUNG FÜR P1-4 ##
  # Umwandeln von alpha (deg) zu alpha (rad)
  alpha_rad = alpha * (math.pi / 180)

  # X & Y offset berechnen

  a = math.cos(alpha_rad) * node_length
  b = math.sin(alpha_rad) * node_length

  # Optionale Debug Infos
  if debug: print(f"Gen: {generation} Alpha: {alpha} a: {round(a)} b: {round(b)}")

  # Berechnen der End-Koordinaten
  P1_x = P1_x
  P1_y = P1_y

  P2_x = P1_x + a
  P2_y = P1_y - b

  P3_x = P1_x + a - b
  P3_y = P1_y - a - b

  P4_x = P1_x - b
  P4_y = P1_y - a

  # Optionale Debug Infos
  if debug and (mode == "quad"): print(f"Gen: {generation} P1({round(P1_x)}|{round(P1_y)}) P2({round(P2_x)}|{round(P2_y)}) P3({round(P3_x)}|{round(P3_y)}) P4({round(P4_x)}|{round(P4_y)})")

  ## Drawing
  # Also das malen dieser Node in die SVG Datei

  ## LINES ##
  if mode == "line":
    draw_line(x1=P1_x, y1=P1_y, x2=P2_x, y2=P2_y, 
              width=(node_length * line_width), 
              colour=colour_lines, 
              comment=f"Gen: {generation}")

  ## QUAD ##
  elif mode == "quad":
    to_file(f'<!-- Gen {generation} Quad -->')
    draw_line(x1=P1_x, y1=P1_y, x2=P2_x, y2=P2_y, 
          width=(node_length * line_width), 
          colour=colour_lines if not debug else "#FF0000", # red
          comment=f"q1; Gen{generation}",
          addtional_option='stroke-linecap="square"')
    draw_line(x1=P2_x, y1=P2_y, x2=P3_x, y2=P3_y, 
          width=(node_length * line_width), 
          colour=colour_lines if not debug else "#00FF00", # green
          comment=f"q2; Gen{generation}",
          addtional_option='stroke-linecap="square"')
    draw_line(x1=P3_x, y1=P3_y, x2=P4_x, y2=P4_y, 
          width=(node_length * line_width), 
          colour=colour_lines if not debug else "#0000FF", # blue
          comment=f"q3; Gen{generation}",
          addtional_option='stroke-linecap="square"')
    draw_line(x1=P4_x, y1=P4_y, x2=P1_x, y2=P1_y, 
          width=(node_length * line_width), 
          colour=colour_lines if not debug else "#FFFF00", # yellow
          comment=f"q4; Gen{generation}",
          addtional_option='stroke-linecap="square"')
    to_file(f'<!-- Gen {generation} Quad End -->')

  ## Generate Children
  if generation < max_generations: # Limitiert die Generationen

    # Spacing errechnen
    if ((spread == 0) or (spread is None)) and mode == "line": child_spacing = 180 / children_count
    else: child_spacing = spread

    for i in range(children_count if (generation != 0) or (initial_children_count is None) else initial_children_count): # Wiederholen für alle children, die generiert werden sollen

      ## LINES ##
      if mode == "line":
        child_rotation = (i+0.5) * child_spacing + alpha - 90
        node(P2_x, P2_y, generation+1, child_rotation, node_length) # Generiert eine neue Node

      ## QUADS ##
      elif mode == "quad":
        match i+1:
          case 1: # links-oben --> an Ecke P4
            child_rotation = 0 + alpha + child_spacing
            node(P4_x, P4_y, generation+1, child_rotation, node_length)
          case 2: # rechts-oben --> an Ecke P3
            child_rotation = 270 + alpha + child_spacing
            node(P3_x, P3_y, generation+1, child_rotation, node_length)
          case 3: # rechts-unten --> an Ecke P2
            child_rotation = 180 + alpha + child_spacing
            node(P2_x, P2_y, generation+1, child_rotation, node_length)
          case 4: # links-unten --> an Ecke P1
            child_rotation = 90 + alpha + child_spacing
            node(P1_x, P1_y, generation+1, child_rotation, node_length)


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
  node((svg_width / 2), svg_height, 0, 0, initial_size*dropoff)
elif start == "mid":
  node((svg_width / 2) - initial_size/2, (svg_height / 2) + initial_size/2, 0, 0, initial_size*dropoff)


## CLEANUP ##
to_file('\n</svg>') # Schreibt den svg footer in die SVG Datei
print("Fertig!")