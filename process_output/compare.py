import nibabel as nib
import numpy as np
import os

# # 输入文件路径
# nii1_path = "./gt/PA000027.nii.gz"
# nii2_path = "./validation/PA000027.nii.gz"

# # 输出文件路径
# output_path = "./merged/PA27.nii.gz"

# # 读取图像
# nii1 = nib.load(nii1_path)
# nii2 = nib.load(nii2_path)

# data1 = nii1.get_fdata().astype(np.uint8)
# data2 = nii2.get_fdata().astype(np.uint8)

# # 合并逻辑
# merged = np.zeros_like(data1, dtype=np.uint8)
# merged[np.logical_and(data1 == 1, data2 == 0)] = 1
# merged[np.logical_and(data1 == 0, data2 == 1)] = 2
# merged[np.logical_and(data1 == 1, data2 == 1)] = 3

# # 保存合并后的结果
# merged_nii = nib.Nifti1Image(merged, affine=nii1.affine, header=nii1.header)
# nib.save(merged_nii, output_path)

# print(f"✅ 合并完成，保存为：{output_path}")

for filename in os.listdir("./validation"):
        if filename.endswith(".nii.gz"):
            
            pred_path = os.path.join("./validation", filename)
            gt_path = os.path.join("./gt", filename)

            # 输出文件路径
            output_path = os.path.join("./merged", filename)

            # 读取图像
            pred = nib.load(pred_path)
            gt = nib.load(gt_path)

            data1 = pred.get_fdata().astype(np.uint8)
            data2 = gt.get_fdata().astype(np.uint8)

            # unique_vals = np.unique(data1)
            # print(f"图像1中包含的值: {unique_vals}")

            # unique_vals = np.unique(data2)
            # print(f"图像2中包含的值: {unique_vals}")

            # 合并逻辑: only in pred => 1, only in gt => 2, coincide => 3
            merged = np.zeros_like(data1, dtype=np.uint8)
            merged[np.logical_and(data1 == 1, data2 == 0)] = 1
            merged[np.logical_and(data1 == 0, data2 == 1)] = 2
            merged[np.logical_and(data1 == 1, data2 == 1)] = 3

            # unique_vals = np.unique(merged)
            # print(f"图像2中包含的值: {unique_vals}")

            # 保存合并后的结果
            merged_nii = nib.Nifti1Image(merged, affine=pred.affine, header=pred.header)
            nib.save(merged_nii, output_path)

            print(f"✅ 合并完成，保存为：{output_path}")