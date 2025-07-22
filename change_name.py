import os

# 替换为你实际的 img 文件夹路径
folder = "./img"

for filename in os.listdir(folder):
    if filename.endswith(".nii.gz"):
        old_path = os.path.join(folder, filename)

        # 拆分文件名与扩展名
        name_without_ext = filename[:-7]  # 去掉 ".nii.gz"
        new_filename = f"{name_without_ext}_0000.nii.gz"
        new_path = os.path.join(folder, new_filename)

        # 重命名
        os.rename(old_path, new_path)
        print(f"✅ 已重命名: {filename} → {new_filename}")
