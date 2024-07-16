import os

folder_path = 'F:\成辉\PDF'
for root, dirs, files in os.walk(folder_path):
    # print(root)
    print(dirs)
    # print(files)
