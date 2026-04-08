import os
import time
import random
import requests
import schedule
import datetime
import smart_open


def log(text, level=0, writes=True):
    level_text = ""
    if level == 0:
        level_text = "INFO"
    elif level == 1:
        level_text = "ERROR"
    elif level == 2:
        level_text = "DEBUG"
    log_text = "[%s %s]%s\n" % (level_text, datetime.datetime.now(), text)
    print(log_text)
    if writes:
        with open(f"plate_log.txt", "a") as f:
            f.write(log_text)


_all_ids = []


def buka(token):
    ls = []
    now_time = datetime.datetime.now()
    log(f" 正在提交广告补卡: {token}")
    for i in range(1, 8):
        day_weekago = (now_time - datetime.timedelta(days=i)).date()
        url = "https://clearplate-api.guangpanxingdong.com/index.php"
        params = {"r": "/user-clear-plate/clear-plate-supplement"}
        payload = {"sup_date": f"{day_weekago}", "is_watch_video": "1"}
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 15) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/134.0.6998.136 Mobile Safari/537.36 XWEB/1340043 MMWEBSDK/20250201 MMWEBID/1424 MicroMessenger/8.0.57.2820(0x28003933) WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64 MiniProgramEnv/android",
            "x-token": token,
            "x-version": "7.9.0",
            "x-access-token": "",
            "x-form-id-list": "[]",
            "x-requested-with": "XMLHttpRequest",
            "x-oauth-type": "1",
            "x-app-platform": "wx",
            "charset": "utf-8",
        }
        response = requests.post(url, params=params, data=payload, headers=headers)
        ls.append(response.text)
        time.sleep(1)
    return ls


def daka(token, longitude_inp, latitude_inp, group_id):
    url = "https://clearplate-api.guangpanxingdong.com/index.php"
    params = {"r": "/user-clear-plate/clear-plate"}
    longitude_inp = float(longitude_inp)
    latitude_inp = float(latitude_inp)
    longitude = random.uniform(
        longitude_inp, longitude_inp + 0.1
    )  # 经度,float,随机取值
    latitude = random.uniform(latitude_inp, latitude_inp + 0.1)
    payload = {
        "group_id": f"{group_id}",  # 组织id
        "path_url": "Photo",
        "location": f"{latitude},{longitude}",
        "ai_type": "",
        "ai_weight": "",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 15) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/134.0.6998.136 Mobile Safari/537.36 XWEB/1340043 MMWEBSDK/20250201 MMWEBID/1424 MicroMessenger/8.0.57.2820(0x28003933) WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64 MiniProgramEnv/android",
        "x-token": token,
        "x-version": "8.0.11",
        "x-access-token": "",
        "x-form-id-list": "[]",
        "x-requested-with": "XMLHttpRequest",
        "x-oauth-type": "1",
        "x-app-platform": "wx",
        "charset": "utf-8",
    }
    response = requests.post(url, params=params, data=payload, headers=headers)
    return response


def load_uid(token):
    global _all_ids
    uid_url = "https://clearplate-api.guangpanxingdong.com/index.php?r=/user/user-info"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 15) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/134.0.6998.136 Mobile Safari/537.36 XWEB/1340043 MMWEBSDK/20250201 MMWEBID/1424 MicroMessenger/8.0.57.2820(0x28003933) WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64 MiniProgramEnv/android",
        "x-token": token,
        "x-version": "8.0.11",
        "x-access-token": "",
        "x-form-id-list": "[]",
        "x-requested-with": "XMLHttpRequest",
        "x-oauth-type": "1",
        "x-app-platform": "wx",
        "charset": "utf-8",
    }
    uid_response = requests.get(uid_url, headers=headers)
    if uid_response.status_code == 200:
        uid_json = uid_response.json()
        data = uid_json["data"]
        nid = data.get("user_id")
        if not nid in _all_ids:
            log(f"已载入用户id:{nid}")
            _all_ids.append(nid)


def zan(token):
    global _all_ids
    print(_all_ids)
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 15) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/134.0.6998.136 Mobile Safari/537.36 XWEB/1340043 MMWEBSDK/20250201 MMWEBID/1424 MicroMessenger/8.0.57.2820(0x28003933) WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64 MiniProgramEnv/android",
        "x-token": token,
        "x-version": "8.0.11",
        "x-access-token": "",
        "x-form-id-list": "[]",
        "x-requested-with": "XMLHttpRequest",
        "x-oauth-type": "1",
        "x-app-platform": "wx",
        "charset": "utf-8",
    }
    zan_url = "https://clearplate-api.guangpanxingdong.com/index.php?r=/user/like"

    for i in _all_ids:
        zan_payload = {"user_id": i}
        zan_response = requests.post(zan_url, headers=headers, data=zan_payload)
        if zan_response.status_code == 200:
            zan_json = zan_response.json()
            log(f"给用户 {i} 点赞完毕。[{zan_json.get("msg")}]")
    return "OK"


def plate(tokens, lo, la, group_id):
    data = daka(tokens, lo, la, group_id)
    log(f" 光盘打卡：Token:{tokens},id:{group_id},请求结果: {data.text}")
    buka_data = buka(tokens)
    log(f" 广告补卡：Token:{tokens},id:{group_id},请求结果: {buka_data}")
    zan_data = zan(tokens)
    log(f" 自动点赞：Token:{tokens},id:{group_id},请求结果: {zan_data}")


def main():
    Token_Data = "tokens.txt"
    try:
        log(" 任务开始运行")
        if os.path.isfile(Token_Data):
            with smart_open.smart_opens(Token_Data, "r") as f:
                tokens = f.read().splitlines()
        else:
            with open(Token_Data, "w") as f:
                f.write(
                    "#本程支持多个Token一起执行;在文件内写入Token,一行一个,井号开头为注释"
                )
            tokens = []
            log(f"已新建Tokens数据文件,请到 {Token_Data} 内填写Tokens")
        # 您需要使用抓包工具抓取x-token和组织ID(手动提交一次光盘并抓包即可得)
        # 组织ID
        group_id = 6372
        # 以下不需要抓取。可用坐标拾取器获取到想要的经纬度
        # 经度
        lon = 118.578482
        # 纬度
        lat = 24.33405
        for i in tokens:  # 先加载一次所有UID
            if not i[0] == "#":
                load_uid(i)
        for i in tokens:  # 执行一次点赞
            if not i[0] == "#":
                zan(i)
        for i in tokens:
            if not i[0] == "#":
                plate(i, "%.6f" % lon, "%.6f" % lat, group_id)
                time.sleep(3)
        else:
            log("任务执行完毕,等待下一周期")
    except Exception as e:
        log(f"运行出现错误,请调试排查。{e}")


if __name__ == "__main__":
    main()
    schedule.every().hour.at(":01").do(main)  # 每个小时01分开始打卡
    while True:
        if datetime.datetime.now().time() > datetime.time(6, 00):
            os.system("title 光盘行动自动打卡")
            schedule.run_pending()
            time.sleep(1)
