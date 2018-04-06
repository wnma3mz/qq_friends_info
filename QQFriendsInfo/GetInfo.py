# coding: utf-8
import requests
import pickle
import time
from datetime import datetime


class GetInfo(object):
    """登陆移动端qq空间获取qq好友资料和加为好友的时间"""

    def __init__(self, qzonetoken, sid, g_tk, myuin):
        """
        初始化请求参数
        Parameters
        ----------
        qzonetoken: str
            登陆手机版qq空间获取到的qzonetoken
        sid: str
            登陆手机版qq空间获取到的sid
        g_tk: str
            登陆手机版qq空间获取到的g_tk
        myuin: str
            本人的qq号

        Returns
        -------
            None
        """
        self.s = requests.session()
        # 初始化请求参数
        self.params = {
            "qzonetoken": qzonetoken,
            "format": "json",
            "sid": sid,
            "g_tk": g_tk,
        }
        self.myuin = myuin

    def __interval_days(self, add_friend_time):
        """
        计算认识天数，用当前时间戳减去加为好友的时间戳
        Parameters
        ----------
        timestamp: timestamp
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

    def __get_add_friend_time(self, friend_uin):
        """
        获取加为好友的时间戳并转换认识天数
        Parameters
        ----------
        friend_uin: str
            好友的QQ号

        Returns
        -------
        int: 
            与好友认识的天数（从加好友的那天算起）
        """
        # 请求的url
        url = "https://mobile.qzone.qq.com/friendship/get_friendship"
        # 请求参数
        self.params["fromuin"] = friend_uin
        self.params["touin"] = self.myuin
        self.params["res_type"] = "4"

        # 尝试获取与好友相关信息资料
        try:
            friendship_res = self.s.get(url, params=self.params).json()["data"]
        except Exception:
            raise TypeError("params is wrong!")

        # 提取加好友的那天的时间戳
        add_friend_time = friendship_res["friendShip"][0]["add_friend_time"]
        # 处理时间戳
        return self.__interval_days(int(add_friend_time))

    def get_friend_profile(self, cookie, friend_uin):
        """
        获取好友资料, 字段是否为空取决于对方给的权限和对方是否填写信息
        Parameters
        ----------
        cookie: str
            请求headers中的cookie
        friend_uin: str
            好友的QQ号

        Returns
        -------
        json: 
            返回好友资料的json信息
            {
                'add_friend_days': 构造的新字段，认识好友的天数
                'age': 0,
                'birthday': 1,
                'birthmonth': 1,
                'birthyear': 0,
                'city': '',
                'cityid': '0',
                'constellation': '', 星座
                'country': '',
                'countryid': '0',
                'face': '', 空间头像
                'gender': -1,
                'isBrandQzone': 0,
                'islunar': 0,
                'limitsMask': 31,
                'nickname': '', 网名
                'province': '',
                'provinceid': '0'
            }
        """
        # 好友资料的url
        url = "https://mobile.qzone.qq.com/profile_get"

        # 去除无必要的参数，虽然不去除也不影响
        keys_lst = ["fromuin", "touin", "res_type"]
        for key in keys_lst:
            if key in self.params.keys():
                self.params.pop(key)

        # 添加请求参数
        self.params["hostuin"] = friend_uin
        headers = {"cookie": cookie}

        profile_res = self.s.get(url, headers=headers, params=self.params)

        # 尝试获取好友资料信息
        try:
            profile_data = profile_res.json()["data"]
        except Exception:
            raise TypeError("cookie is wrong!")

        # 获取与好友认识天数
        days = self.__get_add_friend_time(friend_uin)

        # 在原有好友资料基础上加上新字段"认识天数"
        profile_data["add_friend_days"] = days
        return profile_data
