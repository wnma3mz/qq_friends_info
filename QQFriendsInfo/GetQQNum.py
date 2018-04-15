# coding: utf-8

import requests
import pickle
import re


class GetQQNum(object):
    """获取所有好友的QQ号并保存至本地"""

    def __init__(self, cookie):
        """
        初始化参数
        Parameters
        ----------
        bkn: str
            请求群管理(http://qun.qq.com/cgi-bin/qun_mgr/get_friend_list)页面的bkn
        cookie: str
            请求群管理页面的cookie

        Returns
        -------
        None
        """

        # self.bkn = bkn
        self.cookie = cookie
        self.bkn = self.__get_bkn()
        self.mem_lst = self.__get_uin_lst()

    def __get_bkn(self):

        try:
            skey = re.findall(r"skey.+?;", self.cookie)[0]
            skey = skey.split("=")[-1][:-1]
        except Exception as e:
            raise TypeError("please input correct cookie")

        n = 5381
        e = 0
        o = len(skey)
        while (o > e):
            n += (n << 5) + ord(skey[e])
            e += 1
        return 2147483647 & n

    def __get_uin_lst(self):
        """
        获取qq好友qq号(uin)和对应备注(name), 保存在mem_lst中
        Parameters
        ----------
        None
            
        Returns
        -------
        list:
            [
                {'name': 'aaa', 'uin': 123456},
                {'name': 'bbb', 'uin': 12030},
                {'name': 'ccc', 'uin': 303},
                {'name': 'ddd', 'uin': 341}
            ]
        好友备注名和qq号
        """

        # 请求的url
        url = "http://qun.qq.com/cgi-bin/qun_mgr/get_friend_list"
        # 请求携带的参数
        payload = {"bkn": self.bkn}
        headers = {
            "cookie":
            self.cookie,
            "user-agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        }
        response = requests.post(url, data=payload, headers=headers).json()

        # 如果参数正确应该能够获取到每个分组下的所有好友的信息
        try:
            friends_json = response["result"]
        except Exception:
            raise TypeError("Please input correct params")

        # 遍历每个分组，排除分组为空的情况
        for key in friends_json.keys():
            if not friends_json.get(key, 0):
                del friends_json[key]

        # 取出每个分组中的成员信息
        mem_lst = [
            friend for key, friend_value in friends_json.items()
            for friend in friend_value["mems"]
        ]

        return mem_lst

    def save_data(self, fname):
        """
        保存信息到本地
        Parameters
        ----------
        fname: str
            保存的文件名

        Returns
        -------
        None
        """
        with open(fname, "wb+") as f:
            pickle.dump(self.mem_lst, f)
