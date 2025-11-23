import math

debug = True
file = 'sierpinski.svg'

## SETTINGS ##
# Board
height = 3600
width = 6400

# Sierpinski
max_generations = 10

## SVG STUFF ##
def init_file(filename):
    open(filename, 'w').close()
    to_file(f'<?xml version="1.0" encoding="UTF-8"?>')
    to_file(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">')
    # Hintergrund weiß
    to_file(f'<rect width="{width}" height="{height}" fill="#FFFFFF" />')

def to_file(contents: str):
    try:
        with open(file, 'a') as f:
            f.write(contents + "\n")
    except:
        print("Error writing to svg file!")

def draw_triangle(ax, ay, bx, by, cx, cy, stroke="#000000"):
    #Zeichnet Dreieck als SVG-Polygon
    tri_str = (
        f'<polygon points="'
        f'{ax},{ay} {bx},{by} {cx},{cy}" '
        f'fill="none" stroke="{stroke}" stroke-width="1" />'
    )
    to_file(tri_str)

## SIERPINSKI NUR MIT LINIEN ##
def sierpinski(ax, ay, bx, by, cx, cy, generation):
    if generation == max_generations:
        draw_triangle(ax, ay, bx, by, cx, cy)
        return

    # Mittelpunkte berechnen
    abx = (ax + bx) / 2
    aby = (ay + by) / 2

    bcx = (bx + cx) / 2
    bcy = (by + cy) / 2
    
    cax = (cx + ax) / 2
    cay = (cy + ay) / 2

    if debug:
        print(f"Generation {generation}: "
              f"AB=({abx:.1f},{aby:.1f}), "
              f"BC=({bcx:.1f},{bcy:.1f}), "
              f"CA=({cax:.1f},{cay:.1f})")

    # Rekursion auf die 3 Eckdreiecke – kein "Ausschneiden" in der Mitte
    sierpinski(ax,  ay,  abx, aby, cax, cay, generation + 1)  # oben/links
    sierpinski(abx, aby, bx,  by,  bcx, bcy, generation + 1)  # unten/links
    sierpinski(cax, cay, bcx, bcy, cx,  cy,  generation + 1)  # unten/rechts


########################################################################################################################

## INIT ##
init_file(file)

## GRUNDDREIECK FESTLEGEN ##
side_length = 4000
tri_height = side_length * math.sqrt(3) / 2

top_x = width / 2
top_y = 50                           # etwas Abstand nach oben
left_x = top_x - side_length / 2
left_y = top_y + tri_height
right_x = top_x + side_length / 2
right_y = top_y + tri_height

## SIERPINSKI-REKURSION STARTEN ##
sierpinski(top_x, top_y, left_x, left_y, right_x, right_y, generation=0)

## CLEANUP ##
to_file('</svg>')
print("fertig")
