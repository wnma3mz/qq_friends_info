# coding: utf-8
from QQFriendsInfo import GetQQNum, GetInfo
import pickle

if __name__ == "__main__":
    """
    获取所有QQ好友的QQ号信息, name是备注， uin是好友的QQ号
    [{'name': 'xxx', 'uin': 12345}]
    """
    bkn = ""
    cookie = ""
    mem_lst = GetQQNum(bkn=bkn, cookie=cookie)
    fname = "mem_lst.pkl"
    # 存储数据
    mem_lst.save_data(fname)

    # 读取数据信息
    with open("mem_lst.pkl", "rb") as f:
        mem_lst = pickle.load(f)

    qzonetoken = ""
    sid = ""
    g_tk = ""
    # 本人的QQ号
    myuin = "1234567"
    cookie2 = ""
    # 实例化对象
    mem_info = GetInfo(qzonetoken=qzonetoken, sid=sid, g_tk=g_tk, myuin=myuin)

    lst = []
    # 获取每个好友的资料（前提是对应有权限）, 这里如果请求次数过多，可能会被封一段时间（两个小时）
    for friend in mem_lst:
        # 根据每个好友的QQ号和Cookie
        profile_data = mem_info.get_friend_profile(
            cookie=cookie2, friend_uin=friend["uin"])
        friend["profile_data"] = profile_data
        lst.append(friend)
