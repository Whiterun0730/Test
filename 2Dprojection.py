import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt

#用于将点云2D投影
# Load the point cloud
pcd = o3d.io.read_point_cloud("/home/whiterun/桌面/data/Honda_data/ALL_11A_filtered.xyz")
# Get the points as a numpy array
points = np.asarray(pcd.points)
# Create a 2D projection (e.g., by taking the x and y coordinates)
x = points[:, 0]
y = points[:, 1]
# Plot the projection
plt.scatter(x, y, s=1)
plt.xlabel("X")
plt.ylabel("Y")
plt.title("2D Projection of Point Cloud")
plt.show()
#  xyz_file_path = "/home/whiterun/桌面/data/Honda_data/ALL_11A.xyz"