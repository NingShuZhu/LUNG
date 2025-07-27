import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from PIL import Image
import re

def overlay_additional_mask(
    png_dir,             # 已保存红色叠加切片的文件夹路径
    new_mask_path,       # 另一个mask的nii.gz路径
    output_dir,          # 新保存带蓝色叠加图像的输出文件夹
    axis=2,
    alpha=0.2,
    color='blue'         # 可扩展为其他颜色
):
    os.makedirs(output_dir, exist_ok=True)

    # 加载新的 mask 数据
    mask_img = nib.load(new_mask_path).get_fdata()
    mask_img = np.rot90(mask_img, k=-1, axes=(0, 1))  # 与初始一致

    n_slices = mask_img.shape[axis]

    for i in range(n_slices):
        png_path = os.path.join(png_dir, f"slice_{i:03d}.png")
        if not os.path.exists(png_path):
            continue  # 如果原 PNG 不存在就跳过

        # 加载已有红色叠加切片
        img = np.array(Image.open(png_path))

        # 获取当前切片的 mask
        if axis == 0:
            mask_slice = mask_img[i, :, :]
        elif axis == 1:
            mask_slice = mask_img[:, i, :]
        else:
            mask_slice = mask_img[:, :, i]

        mask_bool = mask_slice > 0.5

        # 构造蓝色覆盖
        color_overlay = np.zeros_like(img)
        if color == 'blue':
            color_overlay[..., 0] = 135  # R
            color_overlay[..., 1] = 206  # G
            color_overlay[..., 2] = 235  # B
        elif color == 'green':
            color_overlay[..., 1] = 255
        else:
            color_overlay[..., 0] = 255  # 默认红色

        blended = img.copy()
        blended[mask_bool] = np.clip(
            blended[mask_bool] + alpha * color_overlay[mask_bool],
            0, 255
        ).astype(np.uint8)

        # 镜像图像
        blended_flipped = np.fliplr(blended)

        # 保存图像
        plt.imsave(os.path.join(output_dir, f"slice_{i:03d}.png"), blended_flipped)

    print(f"🎨 已保存双重叠加图像到: {output_dir}")


# 总目录
existing_png_root = "./merged"
new_mask_root = "./airway_pred"
output_root = "./merged_airway_artery"

for filename in os.listdir("./img"):
    if filename.endswith(".nii.gz"):
        base_name = filename.replace("_0000.nii.gz", "")

        # for PARSE
        match = re.search(r'(\d{3})$', base_name)

        if match:
            folder_name = match.group(1)
            png_folder = os.path.join(existing_png_root, folder_name)
        else:
            print('no such folder')
            exit()
        # png_folder = os.path.join(existing_png_root, base_name)
        new_mask_path = os.path.join(new_mask_root, f"{base_name}.nii.gz")
        output_folder = os.path.join(output_root, base_name)

        if os.path.exists(png_folder) and os.path.exists(new_mask_path):
            overlay_additional_mask(
                png_dir=png_folder,
                new_mask_path=new_mask_path,
                output_dir=output_folder,
                axis=2,
                alpha=0.4,
                color='blue'  # 你也可以传 'green'
            )
