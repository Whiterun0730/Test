import open3d as o3d
import torch
import matplotlib.pyplot as plt
import numpy as np
import os
import argparse
from pytorch3d.structures import Pointclouds
from pytorch3d.renderer import (
    look_at_view_transform,
    FoVOrthographicCameras,
    PointsRasterizationSettings,
    PointsRenderer,
    PointsRasterizer,
    AlphaCompositor
)
#ply渲染出图
def set_device():
    if torch.cuda.is_available():
        device = torch.device("cuda:0")
        torch.cuda.set_device(device)
    else:
        device = torch.device("cpu")
    return device

def read_ply(input_path):
    print("Reading .ply file...")
    pcd = o3d.io.read_point_cloud(input_path)
    points = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors)
    
    return points, colors

def convert_to_tensors(points, colors, device):
    print("Converting to PyTorch tensors...")
    verts = torch.tensor(points, dtype=torch.float32).to(device)
    rgb = torch.tensor(colors, dtype=torch.float32).to(device)
    print(verts,rgb)
    return verts, rgb

def create_point_cloud(verts, rgb):
    return Pointclouds(points=[verts], features=[rgb])

def initialize_camera(device):
    R, T = look_at_view_transform(7,8,-8)
    cameras = FoVOrthographicCameras(device=device, R=R, T=T, znear=0.01)
    return cameras

def create_renderer(cameras):
    raster_settings = PointsRasterizationSettings(
        image_size=1024,
        radius=0.006,
        points_per_pixel=150
    )
    rasterizer = PointsRasterizer(cameras=cameras, raster_settings=raster_settings)
    renderer = PointsRenderer(
        rasterizer=rasterizer,
        compositor=AlphaCompositor()
    )
    return renderer

def render_point_cloud(renderer, point_cloud):
    print("Rendering point cloud...")
    images = renderer(point_cloud)
    return images

def save_image(images, output_path):
    print("Saving rendered image...")
    plt.figure(figsize=(10, 10))
    plt.imshow(images[0, ..., :3].cpu().numpy())
    plt.axis("off")
    plt.savefig(output_path)
    plt.close()
    print(f"Rendered image saved to {output_path}")

def main(input_path):
    device = set_device()
    points, colors = read_ply(input_path)
    verts, rgb = convert_to_tensors(points, colors, device)
    point_cloud = create_point_cloud(verts, rgb)
    cameras = initialize_camera(device)
    renderer = create_renderer(cameras)
    images = render_point_cloud(renderer, point_cloud)
    
    # 确定输出路径
    input_dir = os.path.dirname(input_path)
    output_path = os.path.join(input_dir, "rendered_image_ply.png")
    
    save_image(images, output_path)

if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='Render a point cloud from a .ply file.')
    parser.add_argument('--input', type=str, required=True, help='Path to the input .ply file.')
    args = parser.parse_args()
    
    # 调用主函数
    main(args.input)
