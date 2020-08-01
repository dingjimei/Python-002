import time
import requests
from fake_useragent import UserAgent

ua = UserAgent(verify_ssl=False)
headers = {
'User-Agent' : ua.random,
'Referer' : 'https://shimo.im/dashboard/own'
}

s = requests.Session()
# 会话对象：在同一个 Session 实例发出的所有请求之间保持 cookie， 
# 期间使用 urllib3 的 connection pooling 功能。
# 向同一主机发送多个请求，底层的 TCP 连接将会被重用，从而带来显著的性能提升。
login_url = 'https://shimo.im/lizard-api/auth/password/login'
form_data = {
'mobile': '+8613803093683',
'password':'123456',
}

# post数据前获取cookie
pre_login = 'https://shimo.im/dashboard/own'
pre_resp = s.get(pre_login, headers=headers)

response = s.post(login_url, data=form_data, headers=headers, cookies=s.cookies)
print(response.text)

# 登陆后可以进行后续的请求
url2 = 'https://shimo.im/dashboard/own'

response2 = s.get(url2,headers = headers)
print(f"response2:{response2.text}")
# response3 = newsession.get(url3, headers = headers, cookies = s.cookies)

# with open('profile.html','w+') as f:
    # f.write(response2.text)