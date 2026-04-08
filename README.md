# Auto_Clear_Plate
Python实现自动光盘打卡

目前实现：
每日自动三次打卡、自动提交全部广告补签、每日多个Token之间相互点赞。

使用方法：
本使用方法面向专业人士。

1.git clone本仓库并安装依赖库requirements.txt

2.运行main.py,自动在运行目录生成一个tokens.txt

3.使用抓包工具抓取微信小程序“光盘打卡”的Token，填写在tokens.txt，支持多个Token一行一个。

4.再次运行main.py，即可开始自动打卡，接下来每2小时提交一次请求。

Token抓取方法可参考这个：https://github.com/poboll/clearplate，本仓库不再赘述。
