import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import imageio

def visualize_and_save_gif(weight_map_path, output_dir, gif_path, num, frame_duration=0.2):
    os.makedirs(output_dir, exist_ok=True)
    weight_map_nii = nib.load(weight_map_path)
    weight_map_data = weight_map_nii.get_fdata().astype(np.int32)

    unique_vals = np.unique(weight_map_data)
    print(f"图像中包含的值: {unique_vals}")

    # 颜色映射（0背景，1蓝，2红，3绿）
    # (R,G,B,A)
    color_list = [
        (0, 0, 0, 0),       # 0: 透明或黑
        (0, 0, 1, 1),       # 1: 蓝
        (1, 0, 0, 1),       # 2: 红
        (0, 1, 0, 1),       # 3: 绿
    ]
    cmap = ListedColormap(color_list)

    rotated_data = np.rot90(weight_map_data, k=-1, axes=(0, 1))

    num_slices = rotated_data.shape[2]
    gif_frames = []

    for z in range(num_slices):
        slice_data = rotated_data[:, :, z]

        if np.any(slice_data > 0):  # 只处理非空切片
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.imshow(slice_data, cmap=cmap, interpolation='nearest', vmin=0, vmax=3)
            ax.axis('off')
            ax.set_title(f"Slice {z} - Output {num}")

            # 保存为 PNG
            png_path = os.path.join(output_dir, f"slice_{z:03d}.png")
            plt.savefig(png_path, bbox_inches='tight', pad_inches=0)
            plt.close(fig)

            # 添加到 GIF 帧列表
            gif_frames.append(imageio.v2.imread(png_path))

    # 保存 GIF
    imageio.mimsave(gif_path, gif_frames, duration=frame_duration)
    print(f"✅ 所有切片保存于 {output_dir}")
    print(f"✅ GIF 动画保存为 {gif_path}")

import re

# 根目录（根据你的实际情况修改）
output_slices_root = "./slices"

for filename in os.listdir("./validation"):
        if filename.endswith(".nii.gz"):
            # 去除扩展名
            base_name = filename.replace(".nii.gz", "")
            
            # 提取文件名最后三位（数字）
            match = re.search(r'(\d{3})$', base_name)
            if match:
                folder_name = match.group(1)
                folder_path = os.path.join(output_slices_root, folder_name)
                os.makedirs(folder_path, exist_ok=True)
                print(f"✅ 已创建或已存在文件夹: {folder_path}")
            else:
                print(f"⚠️ 无法提取最后三位数字: {filename}")

            visualize_and_save_gif(
                weight_map_path=os.path.join("./merged", filename),
                output_dir=folder_path,
                gif_path=os.path.join(output_slices_root, f"{base_name}_ani.gif"),
                num=3,
                frame_duration=0.2  # 每帧 200ms
            )
