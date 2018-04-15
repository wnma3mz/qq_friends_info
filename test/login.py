# coding: utf-8
import requests
import matplotlib.pyplot as plt
from PIL import Image
s = requests.session()
headers = {
    "user-agent":
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
}
url = "https://ssl.ptlogin2.qq.com/ptqrshow"
params = {
    "appid": "715030901",
    "e": "2",
    "l": "M",
    "s": "3",
    "d": "72",
    "v": "4",
    "t": "0.32528823112050387",
    "daid": "73",
    "pt_3rd_aid": "0",
}
img = s.request("post", url, params=params, headers=headers)

with open("login.png", "wb+") as fp:
    fp.write(img.content)
#     img.content
img = Image.open("login.png")
plt.figure()
plt.imshow(img)
plt.show()