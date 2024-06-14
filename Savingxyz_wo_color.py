import numpy as np
import os
#用于生成不保存颜色信息的xyz文件
def read_xyz(input_path):
    print("Reading .xyz file...")
    points = np.loadtxt(input_path, delimiter=' ', usecols=(0, 1, 2))
    return points

def save_xyz_wo_colour(output_path, points):
    print("Saving .xyz file...")
    # 只保存前三行的坐标信息
    np.savetxt(output_path, points, fmt='%.2f', delimiter=' ', header='x y z')

    print(f"Point cloud saved to {output_path}")

if __name__ == "__main__":
    # 输入文件路径
    input_file_path = "/home/whiterun/桌面/data/Honda_data/ALL_11A.xyz"
    
    # 读取 .xyz 文件
    points = read_xyz(input_file_path)

    
    # 提取输出文件的路径
    output_path = os.path.splitext(input_file_path)[0] + "_Nocolour.xyz"
    
    # 保存平移后的前三行点云
    save_xyz_wo_colour(output_path, points)
