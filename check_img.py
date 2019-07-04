import os
def check():
    path ='D:\PyCharm\zhku\cnn_captcha-master\sample\\train'
    names = os.listdir(path)
    for name in names:
        print(name)

        if name.split('_')[0].__len__() !=4:
            print(name)
if __name__ == '__main__':
    check()