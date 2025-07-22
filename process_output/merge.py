import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import os

def overlay_mask_on_ct(ct_path, mask_path, output_dir, alpha=0.3, axis=2):
    """
    将mask叠加在CT图像上并保存为PNG序列
    :param ct_path: CT图像的nii.gz路径
    :param mask_path: mask图像的nii.gz路径（0和1）
    :param output_dir: 保存PNG的目录
    :param alpha: 红色叠加透明度，默认0.3
    :param axis: 显示切片的轴向，默认axis=2（axial）
    """
    os.makedirs(output_dir, exist_ok=True)

    # 加载数据
    ct_img = nib.load(ct_path).get_fdata()
    mask_img = nib.load(mask_path).get_fdata()

    ct_img = np.rot90(ct_img, k=-1, axes=(0, 1))
    mask_img = np.rot90(mask_img, k=-1, axes=(0, 1))

    # 标准化 CT 图像
    ct_img = np.clip(ct_img, -1000, 1000)
    ct_img = (ct_img - ct_img.min()) / (ct_img.max() - ct_img.min())
    ct_img = (ct_img * 255).astype(np.uint8)

    # 遍历切片
    n_slices = ct_img.shape[axis]
    for i in range(n_slices):
        if axis == 0:
            ct_slice = ct_img[i, :, :]
            mask_slice = mask_img[i, :, :]
        elif axis == 1:
            ct_slice = ct_img[:, i, :]
            mask_slice = mask_img[:, i, :]
        else:
            ct_slice = ct_img[:, :, i]
            mask_slice = mask_img[:, :, i]

        ct_rgb = np.stack([ct_slice]*3, axis=-1)

        # 红色叠加
        red_overlay = np.zeros_like(ct_rgb)
        red_overlay[..., 0] = 255  # Red

        mask_bool = mask_slice > 0.5
        blended = ct_rgb.copy()
        blended[mask_bool] = (
            (1 - alpha) * ct_rgb[mask_bool] + alpha * red_overlay[mask_bool]
        ).astype(np.uint8)

        # 保存为PNG
        out_path = os.path.join(output_dir, f"slice_{i:03d}.png")
        plt.imsave(out_path, blended)

    print(f"已保存到：{output_dir}")

overlay_mask_on_ct(
    ct_path="img/PA000013_0000.nii.gz",
    mask_path="pred/PA000013.nii.gz",
    output_dir="./merged/013",
    alpha=0.3,        # 红色透明度
    axis=2            # 沿轴切片（0=sagittal, 1=coronal, 2=axial）
)

import re

# 根目录（根据你的实际情况修改）
output_slices_root = "./merged"

for filename in os.listdir("./img"):
        if filename.endswith(".nii.gz"):
            # 去除扩展名
            base_name = filename.replace("_0000.nii.gz", "")
            
            # 提取文件名最后三位（数字）
            match = re.search(r'(\d{3})$', base_name)
            if match:
                folder_name = match.group(1)
                folder_path = os.path.join(output_slices_root, folder_name)
                os.makedirs(folder_path, exist_ok=True)
                print(f"✅ 已创建或已存在文件夹: {folder_path}")
            else:
                print(f"⚠️ 无法提取最后三位数字: {filename}")

            overlay_mask_on_ct(
                ct_path=os.path.join("./img", filename),
                mask_path=os.path.join("./pred", f"{base_name}.nii.gz"),
                output_dir=folder_path,
                alpha=0.2,        # 红色透明度
                axis=2            # 沿轴切片（0=sagittal, 1=coronal, 2=axial）
            )