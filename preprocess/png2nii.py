import os
from PIL import Image
import numpy as np
import nibabel as nib

def convert_ct_png_to_nii(img_path, save_path, normalize=False):
    # 加载灰度图像
    img = Image.open(img_path).convert('L')
    img_array = np.array(img)

    # 可选归一化（0~1 之间），用于浮点表示
    if normalize:
        img_array = img_array.astype(np.float32) / 255.0
    else:
        img_array = img_array.astype(np.uint8)

    # 添加第三个维度，变成 shape: (H, W, 1)
    array_3d = np.expand_dims(img_array, axis=-1)

    # 保存为 NIfTI 格式
    nifti_img = nib.Nifti1Image(array_3d, affine=np.eye(4))
    nib.save(nifti_img, save_path)

def process_ct_folder(input_folder, output_folder, normalize=False):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.png'):
            img_path = os.path.join(input_folder, filename)
            base_name = os.path.splitext(filename)[0]
            save_path = os.path.join(output_folder, base_name + '.nii.gz')

            convert_ct_png_to_nii(img_path, save_path, normalize)
            print(f"Converted: {filename} -> {base_name}.nii.gz")

# ======= 修改这里为你的路径 =======
input_folder = r"./external_img_png"
output_folder = r"./external_img"

# 是否进行0~1归一化（用于深度学习训练时常用）
normalize = False  # 或改为 True

process_ct_folder(input_folder, output_folder, normalize)


