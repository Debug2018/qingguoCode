import string
chars = string.ascii_letters + string.digits
import random
import os
def getrandom():
    return "".join(random.sample(chars, 8))

def concatenate(m):
    return "".join([getrandom() for i in range(m)])

def generate(n):
    return [concatenate(4) for i in range(n)]
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        print(root)  # 当前目录路径
        print(dirs)  # 当前路径下所有子目录
        print(files)  # 当前路径下所有非目录子文件

def re_name():
    n = 0
    files = os.listdir('D:\PyCharm\zhku\cnn_captcha-master\sample\origin')
    for file in files:
        needoldname = files[n][:4]
        oldname = files[n]

        print(oldname)
        newname = needoldname+'_'+generate(1)[0]+'.jpg'
        n += 1
        print(newname)
        os.rename("D:\PyCharm\zhku\cnn_captcha-master\sample\origin\\"+oldname,"D:\PyCharm\zhku\cnn_captcha-master\sample\origin\\"+newname)
    print(files)

if __name__ == '__main__':
    # for item in generate(10):
    #     print(item)
    re_name()
