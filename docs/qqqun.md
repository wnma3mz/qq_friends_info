## 获取请求参数

### 获取bkn和cookie

1. 登陆[QQ群官网](https://qun.qq.com/)
2. 打开浏览器的**开发者选项**(F12), 推荐Chrome或者Firefox。
3. 刷新网页之后，在开发者工具里面，选择**Network**。如下图位置分别找到bkn和cookie，复制到代码中即可。

![qunqq.png](https://raw.githubusercontent.com/wnma3mz/qq_friends_info/master/imgs/qunqq.png)

- 移动端版本: 

    ### 获取qzonetoken, sid, g_tk, cookie2

    1. 登陆[手机QQ版空间](https://mobile.qzone.qq.com/)
    2. 同上操作，获取如下图所示的参数，注: 这里获取到的cookie是cookie2; sid不知道为什么有时候获取不到，可以多刷新几次试试，甚至退出重新登陆

    ![qzone_one.png](https://raw.githubusercontent.com/wnma3mz/qq_friends_info/master/imgs/qzone_one.png)

    myuin指的是自己的QQ号

- PC端版本:

    ### 获取qzonetoken, g_tk, cookie2

    1. 登陆[PC端QQ版空间](https://i.qq.com/)
    2. 同上操作，获取如下图所示的参数，注: 这里获取到的cookie是cookie2

    ![qzone_two.png](https://raw.githubusercontent.com/wnma3mz/qq_friends_info/master/imgs/qzone_two.png)

    myuin指的是自己的QQ号