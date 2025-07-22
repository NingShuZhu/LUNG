import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def visualize_weight_map(weight_map_path, num):
    # 读取 nii.gz 文件
    weight_map_nii = nib.load(weight_map_path)
    weight_map_data = weight_map_nii.get_fdata()
    
    # 提取非零点的位置
    points = np.array(np.where(weight_map_data > 0)).T
    values = weight_map_data[weight_map_data > 0]
    
    # 定义颜色映射
    colors = {1: 'blue', 2:'yellow', 3: 'green'} #, 3: 'yellow', 4: 'orange', 5: 'red'
    point_colors = [colors.get(int(v), 'black') for v in values]
    
    # 创建 3D 图像
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], c=point_colors, s=1, alpha=0.6)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title(f"3D Visualization of output {num}")
    
    plt.show()

#visualize_weight_map("./validation/PA000027.nii.gz", 1)
#visualize_weight_map("./gt/PA000027.nii.gz", 2)
visualize_weight_map("./merged/PA27.nii.gz", 3)