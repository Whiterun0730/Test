file_path = "/home/whiterun/桌面/data/Honda_data/ALL_11A.xyz"
output_file_path = "/home/whiterun/桌面/data/Honda_data/10.xyz"
#xyz仅保存前十行
# 打开原始文件并读取前十行
with open(file_path, 'r') as input_file:
    lines = input_file.readlines()[:10]

# 将前十行写入新文件
with open(output_file_path, 'w') as output_file:
    for line in lines:
        output_file.write(line)
