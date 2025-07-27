import os
from PIL import Image
import numpy as np
import nibabel as nib

def binarize_and_save_nii(img_path, save_path, threshold=128):
    # 读取图像并转为灰度
    img = Image.open(img_path).convert('L')
    img_array = np.array(img)

    # 二值化：大于等于阈值的为1，其他为0
    binary_array = (img_array >= threshold).astype(np.uint8)

    # 添加第三个维度，变成 shape: (H, W, 1)
    array_3d = np.expand_dims(binary_array, axis=-1)

    # 保存为 NIfTI 格式
    nifti_img = nib.Nifti1Image(array_3d, affine=np.eye(4))
    nib.save(nifti_img, save_path)


def process_folder_to_npy(input_folder, output_folder, threshold=128):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.png'):
            img_path = os.path.join(input_folder, filename)
            base_name = os.path.splitext(filename)[0]
            save_path = os.path.join(output_folder, base_name + '.nii')
            
            binarize_and_save_nii(img_path, save_path, threshold)
            print(f"Saved: {save_path}")

# 修改为你的输入文件夹路径
input_folder = r"./labelsTr_org"

# 修改为保存 .npy 文件的输出路径
output_folder = r"./labelsTr1"

process_folder_to_npy(input_folder, output_folder)
