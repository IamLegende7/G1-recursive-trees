import math

file = "koch.svg"

generations = 5

height = 900
width = 1600
boarder = 120

line_width = 1

def init_file(filename):
    open(filename, 'w').close()
    to_file(f'<?xml version="1.0" encoding="UTF-8"?>')
    to_file(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">')
    to_file(f'<rect width="{width}" height="{height}" fill="#FFFFFF" />')

def to_file(contents: str):
    with open(file, 'a') as f:
        f.write(contents + "\n")

def draw_line(x1, y1, x2, y2, width=line_width, color="#000000"):
    line_str = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" />'
    to_file(line_str)

def draw_lines(lines):
    for x1, y1, x2, y2 in lines:
        draw_line(x1, y1, x2, y2)


def split_line(line, segments):
    #Teilt Linie in gleich große Segmente
    x1, y1, x2, y2 = line
    dx = x2 - x1
    dy = y2 - y1

    points = []
    for i in range(segments + 1):
        points.append((
            x1 + dx * (i / segments),
            y1 + dy * (i / segments)
        ))

    # Erzeuge neue Linien
    new_lines = []
    for i in range(segments):
        new_lines.append([
            points[i][0], points[i][1],
            points[i+1][0], points[i+1][1]
        ])

    return new_lines


def rotate60(dx, dy):
    #Dreht Vektor um 60°
    c = 0.5
    s = math.sqrt(3) / 2
    return dx * c - dy * s, dx * s + dy * c


def koch_step(lines):
    # tick
    new_list = []

    for line in lines:
        # Teile die Linie in 3 Segmente
        seg = split_line(line, 3)
        A, B, C = seg  # drei Teilstücke (A:0-1, B:1-2, C:2-3)

        # Punkt B Anfang und Ende
        bx1, by1, bx2, by2 = B

        # Richtungsvektor für Seg B
        dx = bx2 - bx1
        dy = by2 - by1

        # 60° gedrehter Vektor
        rx, ry = rotate60(dx, dy)

        # Spitze des „Dachs“
        px = bx1 + rx
        py = by1 + ry

        # neue Linienfolge für diesen Abschnitt
        new_list.append(A)                                   # Segment 1
        new_list.append([bx1, by1, px, py])                  # Dach links
        new_list.append([px, py, bx2, by2])                  # Dach rechts
        new_list.append(C)                                   # Segment 3

    return new_list


max_h = height - 2 * boarder
side = (2 / math.sqrt(3)) * max_h
h = math.sqrt(3) / 2 * side

cx = width / 2
cy = height / 2

p1 = (cx - side/2, cy + h/3)
p2 = (cx + side/2, cy + h/3)
p3 = (cx,         cy - 2*h/3)

lines = [
    [p1[0], p1[1], p2[0], p2[1]],
    [p2[0], p2[1], p3[0], p3[1]],
    [p3[0], p3[1], p1[0], p1[1]]
]

for i in range(0,generations):
    lines = koch_step(lines)


# Zeichnen
init_file(file)
draw_lines(lines)

to_file("</svg>")
print("fertig")
