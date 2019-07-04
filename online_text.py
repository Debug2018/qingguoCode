import requests
import re
from PIL import Image
import hashlib
import random, string
import datetime
from io import BytesIO
import time
import json
import os
from sample import sample_conf


def MD5(string):
    string = string.encode('gb2312')
    m2 = hashlib.md5()
    m2.update(string)
    return m2.hexdigest()


def randonString():
    return ''.join(random.sample(string.ascii_letters + string.digits, 15))


# 获取密码的加密值
def get_passwd(stu_id, stu_passwd):
    temp = str(MD5(stu_passwd))[0:30].upper() + '11347'
    temp2 = stu_id + temp
    passwd_txt = MD5(temp2)[0:30].upper()
    return passwd_txt


# 获取验证码的加密值
def get_yzm(yzm):
    temp_yzm = MD5(yzm.upper())[0:30].upper() + '11347'
    yzm = MD5(temp_yzm)[0:30].upper()
    return yzm


def logins(username, password):
    s = requests.session()
    img_url = 'http://jw.zhku.edu.cn/sys/ValidateCode.aspx'
    url_login = 'http://jw.zhku.edu.cn/_data/home_login.aspx'
    headerss = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "jw.zhku.edu.cn",
        "Origin": "http://jw.zhku.edu.cn",
        "Referer": "http://jw.zhku.edu.cn/_data/home_login.aspx",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    resp = s.get(url_login, headers=headerss)
    viewstate = re.search(r'<input type="hidden" name="__VIEWSTATE" value="(.*)"', resp.text).group(1)
    cookiejar = resp.cookies
    cookiedict = requests.utils.dict_from_cookiejar(cookiejar)
    cookie = cookiedict['ASP.NET_SessionId']
    cookievalue = 'ASP.NET_SessionId=' + str(cookie)
    headers = {
        'Host': 'jw.zhku.edu.cn',
        'Cookie': cookievalue,
        'Referer': 'http://jw.zhku.edu.cn/_data/home_login.aspx',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    resp = s.get(img_url, headers=headers)


    image_file_name = 'captcha.jpg'
    image_suffix = 'jpg'
    # 识别
    ss = time.time()
    url = "http://127.0.0.1:6000/b"
    files = {'image_file': (image_file_name, BytesIO(resp.content), 'application')}
    r = requests.post(url=url, files=files)
    e = time.time()
    # 新增
    # with open('D:\PyCharm\zhku\cnn_captcha-master\sample\onlines\ss.jpg', 'wb') as f:
    #     f.write(resp.content)
    # 识别结果
    # print("接口响应: {}".format(r.text))
    predict_text = json.loads(r.text)["value"]
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("【{}】 耗时：{}ms 预测结果：{}".format(now_time, int((e - ss) * 1000), predict_text))

    yzm = get_yzm(predict_text)
    passwd = get_passwd(username, password)
    data = {
        '__VIEWSTATE': viewstate,
        'pcInfo': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36undefined5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36 SN:NULL',
        'typeName': 'ѧ��',
        'dsdsdsdsdxcxdfgfg': passwd,
        'fgfggfdgtyuuyyuuckjg': yzm,
        'Sel_Type': 'STU',
        'txt_asmcdefsddsd': username,
        'txt_pewerwedsdfsdff': '',
        'txt_sdertfgsadscxcadsads': '',
    }
    login_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep - alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'jw.zhku.edu.cn',
        'Origin': 'http: // jw.zhku.edu.cn',
        'Cookie': cookievalue,
        'Referer': 'http://jw.zhku.edu.cn/_data/home_login.aspx',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }
    url_login = 'http://jw.zhku.edu.cn/_data/home_login.aspx'

    response = s.post(url_login, data=data, headers=login_headers)
    html = response.text
    if re.search(u"登录失败", html):
        print("请检查用户名,密码及验证码是否错误")
        img_name = "{}_{}.{}".format(predict_text, str(ss).replace(".", ""), image_suffix)
        path = os.path.join("./sample/fail_sample/", img_name)
        with open(path, "wb") as f:
            f.write(resp.content)
        print("============== end ==============")
    elif re.search(u'正在加载权限', html):
        print("验证成功")
        img_name = "{}_{}.{}".format(predict_text, str(ss).replace(".", ""), image_suffix)
        path = os.path.join( "./sample/pass_sample/", img_name)
        with open(path, "wb") as f:
            f.write(resp.content)
        print("============== end ==============")
    else:
        print('发生未知错误请重试')
        img_name = "{}_{}.{}".format(predict_text, str(ss).replace(".", ""), image_suffix)

        path = os.path.join("./sample/fail_sample/", img_name)
        with open(path, "wb") as f:
            f.write(resp.content)
        print("============== end ==============")
def main():
    for i in range(23):
        logins('账号', '密码')
        print("正在进行第{}次验证".format(i+1))



if __name__ == '__main__':
    main()
    #964