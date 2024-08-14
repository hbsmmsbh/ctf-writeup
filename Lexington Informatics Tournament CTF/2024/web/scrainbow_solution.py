from colorsys import rgb_to_hls
import requests

# Function to convert hex color to HSL
def hex_to_hsl(hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    h, l, s = rgb_to_hls(r/255.0, g/255.0, b/255.0)
    return (h, l, s)

# Given color grid, obtain from http://litctf.org:31780/data, stored in scrainbow_grid_data.txt
colors = requests.get("http://litctf.org:31780/data").json()

# Convert hex colors to HSL and sort by Hue
sorted_colors = sorted(colors, key=lambda x: hex_to_hsl(x)[0])

# Rearrange sorted colors diagonally into a 100x100 grid
grid_size = 100
rainbow_grid = [['' for _ in range(grid_size)] for _ in range(grid_size)]

index = 0
for d in range(2 * grid_size - 1):
    for i in range(max(0, d - grid_size + 1), min(grid_size, d + 1)):
        j = d - i
        if i < grid_size and j < grid_size:
            rainbow_grid[i][j] = sorted_colors[index]
            index += 1

# prepare the solution data.
# 1: compare the original grid & final grid.
# 2: if same, then keep it,
# 3: if not, then find the first occurrence of color value after the current position,
#    then swap them.

solution = []
for i in range(grid_size):
    for j in range(grid_size):
        c = rainbow_grid[i][j]
        iii = i*grid_size + j
        if colors[iii] == c:
            # if same, then keep it,
            continue
        else:
            # if not, then find the first occurrence of color value after the current position
            index = colors.index(c, iii + 1)
            # swap them
            tmp = colors[iii]
            colors[iii] = c
            colors[index] = tmp
            solution.append([iii, index])

# send the final solution request to server
payload = {"data": solution}
r = requests.post("http://litctf.org:31780/test", json=payload)
print(r.text)
