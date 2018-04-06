# coding: utf-8
import requests
import pickle
import time
from datetime import datetime


class GetInfoPC(object):
    """登陆PC版qq空间获取qq好友资料和加为好友的时间"""

    def __init__(self, qzonetoken, cookie, g_tk, myuin):
        """
        初始化请求参数
        Parameters
        ----------
        qzonetoken: str
            登陆qq空间获取到的qzonetoken
        cookie: str
            登陆qq空间获取到的cookie
        g_tk: str
            登陆qq空间获取到的g_tk
        myuin: str
            本人的qq号

        Returns
        -------
            None
        """

        self.s = requests.session()
        # 初始化请求参数
        self.myuin = myuin
        self.params = {
            "qzonetoken": qzonetoken,
            "format": "json",
            "g_tk": g_tk,
        }
        self.headers = {
            "cookie": cookie,
        }

    def __interval_days(self, add_friend_time):
        """
        计算认识天数，用当前时间戳减去加为好友的时间戳
        Parameters
        ----------
        add_friend_time: timestamp
            加为好友时间的时间戳

        Returns
        -------
        int: 
            时间戳相减并转换为天数        
        """

        # 将两个时间戳强制转换为整型, 并且转换为utc格式（方便做日期加减运算）
        t1 = datetime.utcfromtimestamp(int(time.time()))
        t2 = datetime.utcfromtimestamp(int(add_friend_time))

        # 两个日期相减，获取相差的天数。t2<t1, 保证天数的准确性；如果用t1-t2可能会导致少一天的情况
        t = -(t2 - t1).days

        return t

    def __get_add_friend_time(self):
        """
        获取加为好友的时间戳并转换认识天数
        Parameters
        ----------
        None

        Returns
        -------
        int: 
            与好友认识的天数（从加好友的那天算起）
        """
        # 请求的url
        url = "https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/friendship/cgi_friendship"

        # 保险起见，清除之前的部分请求参数
        for key in ["uin", "vuin", "fupdate"]:
            if key in self.params.keys():
                self.params.pop(key)

        # 增加请求参数
        self.params["activeuin"] = self.myuin
        self.params["passiveuin"] = self.friend_uin
        self.params["situation"] = "1"

        fs_res = self.s.get(url, headers=self.headers, params=self.params)

        # 尝试获取与好友相关信息资料
        try:
            friendship_res = fs_res.json()["data"]
        except Exception:
            raise TypeError("params is wrong!")

        # 提取加好友的那天的时间戳
        add_friend_time = friendship_res["addFriendTime"]
        # 处理时间戳
        return self.__interval_days(int(add_friend_time))

    def get_friend_profile(self, friend_uin):
        """
        获取好友资料, 字段是否为空取决于对方给的权限和对方是否填写信息
        Parameters
        ----------
        friend_uin: str
            好友的QQ号

        Returns
        -------
        json: 
            返回好友资料的json信息
            {
                'add_friend_days': 构造的新字段，认识好友的天数,                
                'address_type': 0,
                'age': 年龄,
                'age_type': 0,
                'animalsign_type': 0,
                'avatar': 空间头像,
                'birthday': 出生月日,
                'birthday_type': 0,
                'birthyear': 出生年,
                'bloodtype': 0,
                'career': 职业,
                'cb': '',
                'cc': 居住城市？,
                'cco': 居住国家，
                'city': '',
                'company': '',
                'constellation': 3,
                'constellation_type': 0,
                'country': '',
                'cp': '',
                'desc': '',
                'emoji': [],
                'famous_custom_homepage': False,
                'hc': 故乡城市,
                'hco': 故乡省份？,
                'home_type': 0,
                'hp': 故乡国家,
                'is_famous': False,
                'islunar': 0,
                'mailaddr': '',
                'mailcellphone': '',
                'mailname': '',
                'marriage': 3,
                'nickname': 网名,
                'province': '',
                'ptimestamp': 当前请求的时间戳,
                'qzeduexp': [],
                'qzworkexp': [],
                'sex': 2,
                'sex_type': 0,
                'signature': 空间个性签名,
                'spacename': 空间名,
                'uin': 好友QQ号
            }
        """
        # 好友资料的url
        url = "https://h5.qzone.qq.com/proxy/domain/base.qzone.qq.com/cgi-bin/user/cgi_userinfo_get_all"
        self.friend_uin = friend_uin

        # 添加请求参数
        self.params["uin"] = self.friend_uin
        self.params["vuin"] = self.myuin
        self.params["fupdate"] = 1

        profile_res = self.s.get(url, headers=self.headers, params=self.params)

        # 尝试获取好友资料信息
        try:
            profile_data = profile_res.json()["data"]
        except Exception:
            raise TypeError("params is wrong!")

        # 获取与好友认识天数
        days = self.__get_add_friend_time()

        # 在原有好友资料基础上加上新字段"认识天数"
        profile_data["add_friend_days"] = days
        return profile_data
