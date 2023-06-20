import os

output_folder = './'
# 列出錄影目錄中的所有影片文件
files = os.listdir(output_folder)
print(files)
# 按文件創建時間排序
files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(output_folder, x)))
print(files)
# 找到最早創建的影片文件，使用 os.remove() 函數刪除該文件
#if len(files) > max_files:
#    os.remove(os.path.join(output_folder, files[0]))
