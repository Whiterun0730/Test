import open3d as o3d
import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import os
import argparse
#ply dbscan去噪且平移至中心
def read_ply(input_path):
    print("Reading .ply file...")
    pcd = o3d.io.read_point_cloud(input_path)
    points = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors)
    return pcd, points, colors

def dbscan_filter(points, eps=1, min_samples=200):
    print("Performing DBSCAN clustering...")
    db = DBSCAN(eps=eps, min_samples=min_samples)
    labels = db.fit_predict(points)

    # 过滤掉标签为 -1 的点（噪声点）
    mask = labels != -1
    filtered_points = points[mask]
    filtered_labels = labels[mask]
    return filtered_points, mask, filtered_labels

def move_to_origin(points):
    print("Moving point cloud to the origin...")
    center = np.mean(points, axis=0)
    print(f"Original mean: {center}")
    points -= center
    new_center = np.mean(points, axis=0)
    print(f"New mean after moving to origin: {new_center}")
    return points

def save_filtered_ply(filtered_points, colors, mask, input_path):
    print("Saving filtered point cloud...")
    filtered_colors = colors[mask]
    filtered_pcd = o3d.geometry.PointCloud()
    filtered_pcd.points = o3d.utility.Vector3dVector(filtered_points)
    filtered_pcd.colors = o3d.utility.Vector3dVector(filtered_colors)
    
    # 确定新的文件名
    base_name = os.path.splitext(input_path)[0]
    output_path = f"{base_name}_filtered.ply"
    
    o3d.io.write_point_cloud(output_path, filtered_pcd)
    print(f"Filtered point cloud saved to {output_path}")
    return output_path

def plot_clusters(points, labels):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(points[:, 0], points[:, 1], points[:, 2], c=labels, cmap='viridis', s=1)
    legend1 = ax.legend(*scatter.legend_elements(), title="Clusters")
    ax.add_artist(legend1)
    plt.show()

def main(input_path):
    pcd, points, colors = read_ply(input_path)
    
    # 保存原始点云的均值
    original_mean = np.mean(points, axis=0)
    print(f"Original mean of the point cloud: {original_mean}")
    
    filtered_points, mask, labels = dbscan_filter(points)
    
    # 移动过滤后的点云到原点
    filtered_points = move_to_origin(filtered_points)
    
    # 生成聚类结果图
    plot_clusters(filtered_points, labels)
    
    # 用户输入决定是否保存
    save_choice = input("Do you want to save the filtered point cloud and the clustering plot? (y/n): ").strip().lower()
    if save_choice == 'y':
        # 保存过滤后的点云
        output_path = save_filtered_ply(filtered_points, colors, mask, input_path)
        
        # 保存聚类图
        plot_path = os.path.splitext(input_path)[0] + "_clusters.png"
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')
        scatter = ax.scatter(filtered_points[:, 0], filtered_points[:, 1], filtered_points[:, 2], c=labels, cmap='viridis', s=1)
        legend1 = ax.legend(*scatter.legend_elements(), title="Clusters")
        ax.add_artist(legend1)
        plt.savefig(plot_path)
        print(f"Clustering plot saved to {plot_path}")
    else:
        print("Filtered point cloud and clustering plot were not saved.")

if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='Filter a point cloud from a .ply file using DBSCAN clustering.')
    parser.add_argument('--input', type=str, required=True, help='Path to the input .ply file.')
    #parser.add_argument('--eps', type=float, default=1, help='The maximum distance between two samples for one to be considered as in the neighborhood of the other for DBSCAN.')
    #parser.add_argument('--min_samples', type=int, default=1000, help='The number of samples in a neighborhood for a point to be considered as a core point for DBSCAN.')
    args = parser.parse_args()
    
    # 调用主函数
    main(args.input)
