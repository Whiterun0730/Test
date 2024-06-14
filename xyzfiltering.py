import numpy as np
import os
#xyz平移且保存颜色信息
def read_xyz(input_path):
    print("Reading .xyz file...")
    points = np.loadtxt(input_path, delimiter=' ', usecols=(0, 1, 2, 3, 4, 5, 6))
    return points

def move_to_origin(points):
    print("Moving point cloud to the origin...")
    center = np.mean(points[:, :3], axis=0)
    points[:, :3] -= center
    return points

def save_xyz(output_path, points):
    print("Saving .xyz file...")
    # 保存坐标和颜色信息
    np.savetxt(output_path, points, fmt=['%.2f', '%.2f', '%.2f', '%d', '%d', '%d', '%d'], delimiter=' ', header='x y z r g b a')

    print(f"Point cloud saved to {output_path}")

if __name__ == "__main__":
    # 输入文件路径
    input_file_path = "/home/whiterun/桌面/data/Honda_data/ALL_11A.xyz"
    
    # 读取 .xyz 文件
    points = read_xyz(input_file_path)
    
    # 将点云移动到原点
    moved_points = move_to_origin(points)
    
    # 提取输出文件的路径
    output_path = os.path.splitext(input_file_path)[0] + "_filtered.xyz"
    
    # 保存平移后的点云
    save_xyz(output_path, moved_points)
