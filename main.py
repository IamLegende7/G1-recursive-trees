import math

debug = False
file = 'image.svg'

## SETTINGS ##
# General
mode = "line"
submode = None
start = "top"

# Board
svg_height = 900
svg_width = 1600

# Size
initial_size = 200
dropoff = 1.38
line_width = 1/20

# Rotation
spread = None # Not working with lines; keep None for now!

# color
color_background = "#FFFFFF"
color_lines      = "#000000"

# Location
anchor_child = "corner"
anchor_parent = "corner"

# Generations & Children
max_generations = 10
children_count = 2
initial_children_count = None

## SVG STUFF ##
# Diese Funktion schreibt den SVG header und den Hintergrund in die SVG Datei
def init_file(filename):
  open(filename, 'w').close() # SVG Datei leeren
  to_file('<?xml version="1.0" encoding="UTF-8"?>') # xml header
  to_file(f'<svg xmlns="http://www.w3.org/2000/svg" width="{str(svg_width)}" height="{str(svg_height)}">') # svg header

  # Hintergrund
  if not (color_background is None):
    to_file(f'<rect width="{str(svg_width)}" height="{str(svg_height)}" fill="{color_background}" />')
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
              color: str = "#000000",
              comment: str = None,
              additional_option: str = None
              ):
  # Grund-String
  line_str = f'<line x1="{str(x1)}" y1="{str(y1)}" x2="{str(x2)}" y2="{str(y2)}" stroke="{color}" stroke-width="{str(width)}"'
  # Extra optionen
  if not (additional_option is None): line_str = line_str + " " + additional_option

  # Ende line funktion
  line_str = line_str + ' />'

  # Kommentar
  if not (comment is None): line_str = line_str + f' <!-- {comment} -->'
  to_file(line_str)

## NODES ##
def node(origin_x, origin_y, generation, alpha, node_length):
  ## Mathe
  # Umwandeln von alpha (deg) zu alpha (rad)
  alpha_rad = alpha * (math.pi / 180)

  ## BERECHNUNG FÜR P1-4 ##

  # X & Y offset berechnen
  a = math.cos(alpha_rad) * node_length
  b = math.sin(alpha_rad) * node_length

  c = math.cos(alpha_rad) * (node_length / 2)
  d = math.sin(alpha_rad) * (node_length / 2)


  # Optionale Debug Infos
  if debug: print(f"Gen: {generation} Alpha: {alpha} a: {round(a)} b: {round(b)}")

  # Berechnen der Eck-Koordinaten
  if anchor_child == "corner":
    P1_x = origin_x
    P1_y = origin_y
  elif anchor_child == "edge":
    P1_x = origin_x - c
    P1_y = origin_y + d

  P2_x = P1_x + a
  P2_y = P1_y - b

  P3_x = P1_x + a - b
  P3_y = P1_y - a - b

  P4_x = P1_x - b
  P4_y = P1_y - a


  # BERECHNUNG FÜR E1-4 ##
  # E-Punkte sind in der Mitte der Seiten

  # Berechenen
  E1_x = P1_x + c
  E1_y = P1_y - d

  E2_x = P1_x + a - d
  E2_y = P1_y - b - c

  E3_x = P1_x + a - b - c
  E3_y = P1_y - a - b + d

  E4_x = P1_x - b + d
  E4_y = P1_y - a + c

  # Optionale Debug Infos
  if debug and (mode == "quad"): print(f"Gen: {generation} P1({round(P1_x)}|{round(P1_y)}) P2({round(P2_x)}|{round(P2_y)}) P3({round(P3_x)}|{round(P3_y)}) P4({round(P4_x)}|{round(P4_y)})")

  ## Drawing
  # Also das malen dieser Node in die SVG Datei

  ## LINES ##
  if mode == "line":
    draw_line(x1=P1_x, y1=P1_y, x2=P2_x, y2=P2_y, 
              width=(node_length * line_width), 
              color=color_lines, 
              comment=f"Gen: {generation}")

  ## QUAD ##
  elif mode == "quad":
    to_file(f'<!-- Gen {generation} Quad -->')

    draw_line(x1=P1_x, y1=P1_y, x2=P2_x, y2=P2_y, 
          width=(node_length * line_width), 
          color=color_lines if not debug else "#FF0000", # red
          comment=f"q1; Gen{generation}",
          additional_option='stroke-linecap="square"')

    draw_line(x1=P2_x, y1=P2_y, x2=P3_x, y2=P3_y, 
          width=(node_length * line_width), 
          color=color_lines if not debug else "#00FF00", # green
          comment=f"q2; Gen{generation}",
          additional_option='stroke-linecap="square"')

    draw_line(x1=P3_x, y1=P3_y, x2=P4_x, y2=P4_y, 
          width=(node_length * line_width), 
          color=color_lines if not debug else "#0000FF", # blue
          comment=f"q3; Gen{generation}",
          additional_option='stroke-linecap="square"')

    draw_line(x1=P4_x, y1=P4_y, x2=P1_x, y2=P1_y, 
          width=(node_length * line_width), 
          color=color_lines if not debug else "#FFFF00", # yellow
          comment=f"q4; Gen{generation}",
          additional_option='stroke-linecap="square"')

    to_file(f'<!-- Gen {generation} Quad End -->')



  ## Generate Children
  if generation < max_generations: # Limitiert die Generationen
    # Spacing errechnen
    if (spread is None) or mode == "line": child_spacing = 180 / children_count
    else: child_spacing = spread

    # Länge der Child nodes Berechnen
    child1_length = node_length / dropoff

    ## Aussuchen der child spawns ##
    if anchor_parent == "corner":
      C1_x = P4_x # Also: child 1 wird bei P4 generiert
      C1_y = P4_y

      C2_x = P3_x
      C2_y = P3_y

      C3_x = P2_x
      C3_y = P2_y

      C4_x = P1_x
      C4_y = P1_y

    elif anchor_parent == "edge":
      C1_x = E4_x # Also: child 1 wird bei Q4 generiert
      C1_y = E4_y

      C2_x = E3_x
      C2_y = E3_y

      C3_x = E2_x
      C3_y = E2_y

      C4_x = E1_x
      C4_y = E1_y

    # Rotation
    r1 = 0
    r2 = 270
    r3 = 180
    r4 = 90

    if submode == "pythagoras":
      child2_length = math.sin(child_spacing * (math.pi / 180)) * node_length
      beta = 180 - child_spacing - (math.asin(child1_length / node_length) * (180 / math.pi))     # 180° - child_spacing - gamma = beta, denn alpha + beta + gamma = 180°

      if debug: print(f'Alpha: {round(alpha)} Beta: {round(beta)} Gamma: {round(math.asin(child1_length / node_length) * (180 / math.pi))} Spacing: {round(child_spacing)}')

      child_a = math.cos((r1 + alpha + child_spacing) * (math.pi / 180)) * child1_length
      child_b = math.sin((r1 + alpha + child_spacing) * (math.pi / 180)) * child1_length

      C1_P2_x = C1_x + child_a
      C1_P2_y = C1_y - child_b

      C2_P2_x = C2_x + child_b
      C2_P2_y = C2_y + child_a

      C3_P2_x = C3_x - child_a
      C3_P2_y = C3_y + child_b

      C4_P2_x = C4_x - child_b
      C4_P2_y = C4_y - child_a

    for i in range(children_count if (generation != 0) or (initial_children_count is None) else initial_children_count): # Wiederholen für alle children, die generiert werden sollen

      ## LINES ##
      if mode == "line":
        child_rotation = (i+0.5) * child_spacing + alpha - 90
        node(P2_x, P2_y, generation+1, child_rotation, child1_length) # Generiert eine neue Node

      ## QUADS ##
      elif mode == "quad":
        match i+1:
          case 1: # links-oben --> an Ecke P4 / Seite E4
            node(C1_x, C1_y, generation+1, r1 + alpha + child_spacing, child1_length)
            if submode == "pythagoras": node(C1_P2_x, C1_P2_y, generation+1, (child_spacing + alpha + (beta - 180) + r1), child2_length)
          case 2: # rechts-oben --> an Ecke P3 / Seite E3
            node(C2_x, C2_y, generation+1, r2 + alpha + child_spacing, child1_length)
            if submode == "pythagoras": node(C2_P2_x, C2_P2_y, generation+1, (child_spacing + alpha + (beta - 180) + r2), child2_length)
          case 3: # rechts-unten --> an Ecke P2 / Seite E2
            node(C3_x, C3_y, generation+1, r3 + alpha + child_spacing, child1_length)
            if submode == "pythagoras": node(C3_P2_x, C3_P2_y, generation+1, (child_spacing + alpha + (beta - 180) + r3), child2_length)
          case 4: # links-unten --> an Ecke P1 / Seite E1
            node(C4_x, C4_y, generation+1, r4 + alpha + child_spacing, child1_length)
            if submode == "pythagoras": node(C4_P2_x, C4_P2_y, generation+1, (child_spacing + alpha + (beta - 180) + r4), child2_length)


#####################
# EIGENTLICHER CODE #
#####################

## INIT ##
init_file(file)

## GENERATING TREE ##
# Mothernode Einstellungen
if (mode == "quad") and (anchor_child != "edge"): startx = (svg_width / 2) - (initial_size / 2)
else:                                             startx = (svg_width / 2)

if start == "top":
  starty = 0
elif start == "mid":
  if mode == "quad": starty = (svg_height / 2) + (initial_size / 2)
  else:              starty = svg_height / 2
elif start == "bottom":
  starty = svg_height

# Aufrufen der Mothernode
node(origin_x=startx,
     origin_y=starty,
     generation=0,
     alpha=0,
     node_length=initial_size)


## CLEANUP ##
to_file('\n</svg>') # Schreibt den svg footer in die SVG Datei
print("Fertig!")