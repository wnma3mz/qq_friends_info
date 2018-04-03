# coding: utf-8
import requests
import pickle
import time
from datetime import datetime

class GetInfo(object):
    def __init__(self, qzonetoken, sid, g_tk, myuin):
        """
        初始化参数

        myuin: 本人的qq号
        """

        # 初始化请求参数
        self.params = {
            "qzonetoken": qzonetoken,
            "format": "json",
            "sid": sid,
            "g_tk": g_tk,
        }
        self.myuin = myuin

    def __interval_days(self, timestamp):
        """
        计算认识天数，用当前时间戳减去加为好友的时间戳
        """
        t1 = int(time.time())
        t2 = int(timestamp)

        t = datetime.utcfromtimestamp(t2) - datetime.utcfromtimestamp(t1)

        return -t.days

    def __get_add_friend_time(self, friend_uin):
        """
        获取加为好友的时间戳
        """
        # 请求的url
        url = "https://mobile.qzone.qq.com/friendship/get_friendship"
        # 请求参数
        self.params["fromuin"] = friend_uin
        self.params["touin"] = self.myuin
        self.params["res_type"] = "4"

        # 尝试获取加为好友的时间戳，如果获取失败就报错
        try:
            friendship_json = requests.get(url, params=self.params).json()
            timestamp = friendship_json["data"]["friendShip"][0][
                "add_friend_time"]
        except Exception:
            raise TypeError("params is wrong!")

        return self.__interval_days(int(timestamp))

    def get_friend_profile(self, cookie, friend_uin):
        """

        获取好友资料, 字段是否为空取决于对方给的权限

        {'age': 0,
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
        'provinceid': '0'}
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
        try:
            profile_res = requests.get(
                url, headers=headers, params=self.params)
            profile_data = profile_res.json()["data"]
        except Exception:
            raise TypeError("cookie is wrong!")

        # 在原有基础上添加认识天数
        days = self.__get_add_friend_time(friend_uin)

        profile_data["add_friend_days"] = days
        return profile_data
