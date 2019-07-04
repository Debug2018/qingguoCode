import requests
import datetime
import requests
from io import BytesIO
import time
import json
import os
from sample import sample_conf
from PIL import Image
def get_img():
    fail_path = "./sample/fail_sample/"
    pass_path = "./sample/pass_sample/"
    correction_times = 10
    remote_url = "http://jw.zhku.edu.cn/sys/ValidateCode.aspx"


    url = 'http://jw.zhku.edu.cn/sys/ValidateCode.aspx'
    for i in range(100):
        resp = requests.get(url)
        with open('./img/{}.jpg'.format(i),'wb') as f:
            f.write(resp.content)
        print(i)



def recognize_captcha(remote_url, rec_times, save_path, image_suffix):
    image_file_name = 'captcha.{}'.format(image_suffix)

    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    }

    for index in range(rec_times):
        # 请求
        while True:
            try:

                response = requests.request("GET", remote_url, headers=headers, timeout=6)
                if response.text:
                    break
                else:
                    print("retry, response.text is empty")
            except Exception as ee:
                print(ee)

        # 识别
        s = time.time()
        url = "http://127.0.0.1:6000/b"
        files = {'image_file': (image_file_name, BytesIO(response.content), 'application')}
        r = requests.post(url=url, files=files)
        e = time.time()
        #新增
        with open('D:\PyCharm\zhku\cnn_captcha-master\sample\onlines\ss.jpg','wb' ) as f:
            f.write(response.content)
        # 识别结果
        # print("接口响应: {}".format(r.text))
        predict_text = json.loads(r.text)["value"]
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("【{}】 index:{} 耗时：{}ms 预测结果：{}".format(now_time, index, int((e - s) * 1000), predict_text))

        fail_path = "./sample/fail_sample/"
        pass_path = "./sample/pass_sample/"
        # 保存文件
        bool =input("是否正确：")
        #判断错误修改后保存
        n = time.time()
        if bool:
            true_text =input("输入正确的值：")
            img_name = "{}_{}.{}".format(true_text, str(n).replace(".", ""), image_suffix)
            temp_name = "{}_{}.{}".format(predict_text, str(n).replace(".", ""), image_suffix)

            path = os.path.join("./sample/fail_sample/", img_name)
            with open(path, "wb") as f:
                f.write(response.content)
            print("============== end ==============")
            os.remove('D:\PyCharm\zhku\cnn_captcha-master\sample\onlines\ss.jpg')

        #判断正确直接保存
        else:
            img_name = "{}_{}.{}".format(predict_text, str(n).replace(".", ""), image_suffix)
            path = os.path.join(save_path, img_name)
            with open(path, "wb") as f:
                f.write(response.content)
            print("============== end ==============")
            os.remove('D:\PyCharm\zhku\cnn_captcha-master\sample\onlines\ss.jpg')

def main():
    # 配置相关参数
    save_path = "./sample/pass_sample/"  # 下载图片保存的地址
    remote_url = sample_conf["remote_url"]  # 网络验证码地址
    image_suffix = sample_conf["image_suffix"]  # 文件后缀
    rec_times = 1000
    recognize_captcha(remote_url, rec_times, save_path, image_suffix)

if __name__ == '__main__':
    main()

