import os
from datetime import datetime

# print(dir(os))
# print(os.getcwd())
# os.chdir('C:/Users/Asus\Desktop/Data_Science/Data_Science_repo/Flask')
# print(os.getcwd())
# print(os.listdir())
# os.mkdir('test/t') # not possible for deeper
# os.makedirs('test/t') # possible for deeper
# print(os.listdir())
# os.rmdir() # not possible for deeper, and better preffered
# os.removedirs() # possible for deeeper
# print(os.listdir())
# os.rename('t.txt','tt.txt')
# print(os.listdir())
# print(os.stat('tt.txt')) # information about the file
# print(datetime.fromtimestamp(os.stat('tt.txt').st_mtime)) # modification time
# for dirpath, dirnames, filenames in os.walk('C:/Users/Asus/Desktop/Data_Science/Data_Science_repo/Flask'):
#     print('Current Path: ',dirpath)
#     print('Directories: ', dirnames)
#     print('Filename: ', filenames)
#     print()

# file_path = os.path.join(os.getcwd(),'hi','hi')
# print(file_path)

print(os.path.basename('temp/test.txt'))
print(os.path.dirname('temp/test.txt'))
print(os.path.split('temp/test.txt'))
print(os.path.exists('tt.txt'))
print(os.path.isdir('tt.txt'))
print(os.path.isfile('tt.txt'))
print(os.path.splitext('test.txt')) # returns a tuple


