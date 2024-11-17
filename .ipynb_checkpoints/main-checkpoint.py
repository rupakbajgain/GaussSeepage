import numpy as np
import matplotlib.pyplot as plt

# Domain parameters
L_x = 1  # Length of the domain in meters
L_y = 1  # Height of the domain in meters
nx = 100  # Number of points in x-direction (for 0 to 5 meters)
ny = 100  # Number of points in y-direction (for 0 to 5 meters)
dx = L_x / (nx - 1)
dy = L_y / (ny - 1)

# Initialize the grid for hydraulic head (h)
h = np.zeros((ny, nx))  # Hydraulic head grid
k = np.ones((ny, nx))  # Transmisivity grid // 1 full, 0 block flow // simplified with 1 can use fractions


# Sheet plate at x = 2.5 (middle of the sandbox)
sheet_x_index = nx // 2  # The x position of the sheet at x = 2.5
sheet_y_index = ny // 32 #try small sheet
sheet_y_index_start = 0  # The sheet spans from y=0 to y=2.5 //--?

# Boundary conditions:
# Left boundary: h = 10 + y
mode = 0
if mode==0:
    h[0, 0:sheet_x_index] = 10
    h[0, sheet_x_index+1:-1] = 5
elif mode==1:
    h[1, 1:sheet_x_index] = 10
    h[1, sheet_x_index+1:-1] = 5
    #dont let it flow from border too
    k[0,0:-1]=0
    k[-1,0:-1]=0
    k[0:-1,0]=0
    k[0:-1,-1]=0
    k[-1,-1]=0

#pipe
k[0:sheet_y_index, sheet_x_index] = 0

plt.imshow(h)
plt.colorbar()
plt.show()
plt.imshow(k)
plt.colorbar()
plt.show()
#exit()

# Iteration parameters
max_iter = 1000
tolerance = 1e-3#changed i want fast

# Gauss-Seidel Iteration
for it in range(max_iter):
    h_old = h.copy()  # Keep a copy of the current grid for convergence check
    for i in range(1, ny - 1):
        for j in range(1, nx - 1):
            h[i, j] = k[i + 1, j]*h[i + 1, j] + k[i - 1, j]*h[i - 1, j] + k[i , j+1]*h[i, j + 1] + k[i, j - 1]*h[i, j - 1]
            h[i, j] = h[i, j]/(k[i + 1, j]+k[i - 1, j]+k[i , j+1]+k[i, j - 1])
    # Check for convergence (absolute difference)
    if np.max(np.abs(h - h_old)) < tolerance:
        print(f"Converged after {it + 1} iterations.")
        break

#for i in range(1, ny - 1):
#    for j in range(1, nx - 1):
#        h[i, j] = h[i, j]*k[i,j]


plt.imshow(h)
plt.colorbar()
plt.show()

exit()


# Calculate the gradient of the hydraulic head to determine flow direction
# Flow is perpendicular to the equipotential lines (i.e., the gradient of h)
hx, hy = np.gradient(h, dx, dy)

# Plot the results
Y, X = np.meshgrid( np.linspace(- L_y,0, ny),np.linspace(-0.5 * L_x, 0.5 * L_x, nx))

# Plot the contour map (equipotential lines)
plt.figure(figsize=(8, 6))
contour = plt.contourf(X, Y, h[:,::-1], 20, cmap="viridis", origin="upper")
plt.colorbar(contour, label="Hydraulic Head (m)")

# Plot the flow lines (streamlines)
# plt.streamplot(X, Y, -hx, -hy, color='w', linewidth=1)

# Plotting details
# plt.title("Soil Seepage - Hydraulic Head Distribution with Flow and Sheet Plate")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.savefig("Seepage.png")
