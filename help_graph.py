def generate_diagonal_grid():
    # Initialize the grid
    grid = []

    # The starting point
    x1, x2, x3 = 8, 0, 0

    # Go up
    for i in range(6):
        row = []
        new_x1, new_x2, new_x3 = x1 - i, x2 + i, x3
        # Go left
        for j in range(4):
            row.append((new_x1 - j, new_x2, new_x3 + j))
        # Go right and up
        if i > 0:
            new_x1, new_x2, new_x3 = x1 - i, x2, x3 + 1
            for j in range(1, 5):
                row.append((new_x1 - j, new_x2 + j, new_x3))
        grid.append(row)

    return grid


# Generate the grid
grid = generate_diagonal_grid()

# Output the grid
for row in grid:
    print(row)
