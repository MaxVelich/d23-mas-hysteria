
print("Test file")

def get_line_parameters_through_points(point_1, point_2):

    x_1, y_1 = point_1
    x_2, y_2 = point_2

    k = (y_2 - y_1) / (x_2 - x_1)
    d = y_1 - (k * x_1)

    return (k, d)

print(get_line_parameters_through_points((1,1), (3, 2)))