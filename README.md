## 获取所有好友的QQ资料

基于QQ的坦白说活动，活动中会给出好友的两个特征信息，如相识天数、城市、星座等信息，来猜测是哪个好友。本项目可以提取所有QQ好友的个人资料。

目前实现的功能有：

1. 基于bkn, cookie获取所有的qq好友的qq号和备注名，并保存数据到本地

2. 基于qzonetoken, cookie等信息，获取所有qq好友的个人资料（包括相识天数）

### 操作示范

[test/test.py](https://github.com/wnma3mz/qq_friends_info/blob/master/test/test.py)

### 注意事项

如果请求好友资料次数过多(`GetInfo`或`GetInfoPC`), 可能会导致QQ短暂被封

### 使用到的QQ接口

获取好友列表的url: `http://qun.qq.com/cgi-bin/qun_mgr/get_friend_list`

QQ空间移动端版本

- 获取加为好友的时间戳: `https://mobile.qzone.qq.com/friendship/get_friendship`

- 获取好友个人资料（前提是好友给予了权限）: `https://mobile.qzone.qq.com/profile_get`

QQ空间PC端版本

- 获取加为好友的时间戳: `https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/friendship/cgi_friendship`

- 获取好友个人资料（前提是好友给予了权限）: `https://h5.qzone.qq.com/proxy/domain/base.qzone.qq.com/cgi-bin/user/cgi_userinfo_get_all`

### TO-DO

- [ ] 增加模拟登陆

- [ ] 完整思路分享

- [ ] 获取请求参数的文档

- [ ] 输入两个特征，返回符合条件的好友。