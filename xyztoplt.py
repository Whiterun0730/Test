import os
import numpy as np
from plyfile import PlyData, PlyElement
#将xyz传唤成ply形式
def xyz_to_ply(xyz_file, ply_file):
    # 读取xyz文件
    xyz_data = np.loadtxt(xyz_file)
    
    # 创建包含颜色信息的PlyElement
    vertices = np.array([tuple(point) for point in xyz_data], 
                        dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4'),
                               ('red', 'u1'), ('green', 'u1'), ('blue', 'u1'), ('alpha', 'u1')])
    ply_element = PlyElement.describe(vertices, 'vertex')
    
    # 写入ply文件
    PlyData([ply_element]).write(ply_file)
    
    print(f"Converted {xyz_file} to {ply_file}")

input_file_path = '/home/whiterun/桌面/data/Honda_data/ALL_11A.xyz'
output_path = os.path.splitext(input_file_path)[0] + ".ply"
# 使用示例
xyz_to_ply(input_file_path,output_path)
