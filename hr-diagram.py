import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

stars_csv = pd.read_csv('/')

# Arrays to be used in the for loop
star_type = stars_csv['Star type'].values
temperature = stars_csv['Temperature (K)'].values
abs_mag = stars_csv['Absolute magnitude(Mv)'].values
radius = stars_csv['Radius(R/Ro)'].values
spectral_class = stars_csv['Spectral Class'].values

#Dictionary for stars color
stars_color = {
    "O": "#4B73FF",
    "B": "#6A9CFF",
    "A": "#AFCFFF",  
    "F": "#F0F8FF",
    "G": "#FFD27F",
    "K": "#FF8C42",
    "M": "#FF4500"
}

#Function for mapping the radius with pixel size
pixels_max = 8000
pixels_min = 1000
radius_max = max(radius)
radius_min = min(radius)

def map_radius_to_pixels(radius):
  return np.interp(radius, [radius_min, radius_max], [pixels_min, pixels_max])

#Function for drawing spheres
def drawSphere(xCenter, yCenter, zCenter, r):
  u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
  x = np.cos(u) * np.sin(v)
  y = np.sin(u) * np.sin(v)
  z = np.cos(v)
  x = r * x + xCenter
  y = r * y + yCenter
  z = r * z + zCenter

  return x, y, z

#Start the diagram
plt.style.use('dark_background')

axes = []

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

#Add all starts to the plot
for i in range(len(star_type)):
  center = (temperature[i], abs_mag[i]*1000, radius[i]*20)
  sphere_size = map_radius_to_pixels(radius[i])
  color = stars_color.get(spectral_class[i], "#FFFFFF")

  (x,y,z) = drawSphere(center[0], center[1], center[2], sphere_size)

  ax.plot_surface(x, y, z, color=color, alpha=0.7)

#Add legends
patches = [mpatches.Patch(color=stars_color[label], label=label) for label in stars_color]
ax.legend(handles=patches, title="Spectral class", loc='upper right', fontsize=10, ncol=2)

#Invert axis
ax.invert_xaxis()
ax.invert_yaxis()

#Add labels and title
ax.set_xlabel('Temperature (K)', fontsize=12, color='sandybrown', labelpad=5)
ax.set_ylabel('Absolute magnitude (Mv)', fontsize=12, color='sandybrown', labelpad=5)
ax.set_zlabel('Radius (R/Ro)', fontsize=12, color='sandybrown', labelpad=-10)
ax.set_title(f"3D Hertzsprung-Russell diagram for {len(star_type)} stars", fontsize=15, color='white', fontweight=600)

#Show the diagram
plt.show()