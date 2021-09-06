from turtle import *
from math import tan, sin, cos, sqrt
from time import perf_counter

# Initialise Objects and Setup
turtle = Turtle()
turtle.hideturtle()
screen = Screen()
screen.tracer(0)

# Normalised mesh coordinates for drawing the cube
mesh_cube = [
    # North
    [(0, 0, 0), (0, 1, 0), (1, 1, 0), (0, 0, 0)],
    [(0, 0, 0), (1, 1, 0), (1, 0, 0), (0, 0, 0)],
    # South
    [(0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 0, 1)],
    [(0, 0, 1), (1, 1, 1), (0, 1, 1), (0, 0, 1)],
    # East
    [(1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 0)],
    [(1, 0, 0), (1, 1, 1), (1, 0, 1), (1, 0, 0)],
    # West
    [(0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 0, 0)],
    [(0, 0, 0), (0, 1, 1), (0, 1, 0), (0, 0, 0)],
    # Top
    [(0, 1, 0), (0, 1, 1), (1, 1, 1), (0, 1, 0)],
    [(0, 1, 0), (1, 1, 1), (1, 1, 0), (0, 1, 0)],
    # Bottom
    [(0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 0)],
    [(0, 0, 0), (1, 0, 1), (0, 0, 1), (0, 0, 0)],
]


# Function for drawing triangles with Turtle Graphics.
def draw_triangle(start_vector, vector1, vector2, vector3):
    turtle.penup()
    turtle.goto(start_vector)
    turtle.pendown()
    turtle.fillcolor("#ba135d")
    turtle.begin_fill()
    turtle.goto(vector1)
    turtle.goto(vector2)
    turtle.goto(vector3)
    turtle.end_fill()


# Function for drawing the 3D cube on the screen.
def draw_qube(mesh):
    # Clear Screen
    turtle.clear()

    # Projection Calculation Parameters
    width = screen.window_width()
    height = screen.window_height()
    a = width / height  # Aspect Ratio
    fov = 90  # Field of View Angle
    f = 1 / tan(fov * 0.5 / 180 * 3.14159)  # Field of View
    z_near = 1
    z_far = 1000
    q = z_far / (z_far - z_near)  # Z Coordinate Normalisation

    # Qube X-Axis Rotation Calculation
    theta = perf_counter()

    x_rotated_mesh = []
    x_rotated_vector = []

    for tuple_list in mesh:
        x_rotated_mesh.append(x_rotated_vector)
        x_rotated_vector = []
        for vector in tuple_list:
            rotated_x = vector[0]
            rotated_y = vector[1] * cos(theta / 2) - vector[2] * sin(theta / 2)
            rotated_z = vector[1] * sin(theta / 2) + vector[2] * cos(theta / 2)
            x_rotated_vector.append([rotated_x, rotated_y, rotated_z])

    x_rotated_mesh.append(x_rotated_vector)
    x_rotated_mesh.pop(0)

    # Qube Z-Axis Rotation Calculation
    # xz_rotated_mesh = []
    # xz_rotated_vector = []
    #
    # for tuple_list in x_rotated_mesh:
    #     xz_rotated_mesh.append(xz_rotated_vector)
    #     xz_rotated_vector = []
    #     for vector in tuple_list:
    #         rotated_x = vector[0] * cos(theta / 3) - vector[1] * sin(theta / 3)
    #         rotated_y = vector[0] * sin(theta / 3) + vector[1] * cos(theta / 3)
    #         rotated_z = vector[2]
    #         xz_rotated_vector.append([rotated_x, rotated_y, rotated_z])
    #
    # xz_rotated_mesh.append(xz_rotated_vector)
    # xz_rotated_mesh.pop(0)

    # Qube Y-Axis Rotation Calculation
    xzy_rotated_mesh = []
    xzy_rotated_vector = []

    for tuple_list in x_rotated_mesh:
        xzy_rotated_mesh.append(xzy_rotated_vector)
        xzy_rotated_vector = []
        for vector in tuple_list:
            rotated_x = vector[2] * sin(theta) + vector[0] * cos(theta)
            rotated_y = vector[1]
            rotated_z = vector[2] * cos(theta) - vector[0] * sin(theta)
            xzy_rotated_vector.append([rotated_x, rotated_y, rotated_z])

    xzy_rotated_mesh.append(xzy_rotated_vector)
    xzy_rotated_mesh.pop(0)

    # Translation Calculation
    translated_mesh = []
    translated_vector = []

    for tuple_list in xzy_rotated_mesh:
        translated_mesh.append(translated_vector)
        translated_vector = []
        for vector in tuple_list:
            translated_z = vector[2] + 5
            translated_vector.append((vector[0], vector[1], translated_z))

    translated_mesh.append(translated_vector)
    translated_mesh.pop(0)

    # Normal Calculation
    for tuple_list in translated_mesh:
        # Line 1
        line1_x = tuple_list[1][0] - tuple_list[0][0]
        line1_y = tuple_list[1][1] - tuple_list[0][1]
        line1_z = tuple_list[1][2] - tuple_list[0][2]

        # Line 2
        line2_x = tuple_list[2][0] - tuple_list[0][0]
        line2_y = tuple_list[2][1] - tuple_list[0][1]
        line2_z = tuple_list[2][2] - tuple_list[0][2]

        # Calculate Normal
        normal_x = line1_y * line2_z - line1_z * line2_y
        normal_y = line1_z * line2_x - line1_x * line2_z
        normal_z = line1_x * line2_y - line1_y * line2_x

        # Normalise Normal
        length = sqrt(normal_x * normal_x + normal_y * normal_y + normal_z * normal_z)

        normal_x = normal_x / length
        normal_y = normal_y / length
        normal_z = normal_z / length

        tuple_list.append((normal_x, normal_y, normal_z))

    # Projection Calculation
    projected_mesh = []
    projected_vector = []

    for tuple_list in translated_mesh:
        projected_mesh.append(projected_vector)
        projected_vector = []
        for index, vector in enumerate(tuple_list):
            if index == 4:
                projected_vector.append(vector)
                break
            elif vector[2] != 0:
                projected_x = (a * f * vector[0]) / vector[2]
                projected_y = (f * vector[1]) / vector[2]
            else:
                projected_x = (a * f * vector[0])
                projected_y = (f * vector[1])
            projected_z = (vector[2] * q) - (z_near * q)
            # Scaling for Screen Size
            projected_vector.append((projected_x / 2 * width, projected_y / 2 * height))

    projected_mesh.append(projected_vector)
    projected_mesh.pop(0)

    # Drawing the triangles
    camera = (0, 0, 0)
    for index, projected_vector_list in enumerate(projected_mesh):
        # Culling Calculation
        if projected_vector_list[4][0] * (translated_mesh[index][0][0] - camera[0]) + \
                projected_vector_list[4][1] * (translated_mesh[index][0][1] - camera[1]) + \
                projected_vector_list[4][2] * (translated_mesh[index][0][2] - camera[2]) < 0:
            draw_triangle(projected_vector_list[0], projected_vector_list[1], projected_vector_list[2],
                          projected_vector_list[3])

    # Update screen after all triangles are drawn.
    screen.update()


# Main Loop
while True:
    draw_qube(mesh_cube)
