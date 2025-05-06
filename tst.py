# -*- coding: utf-8 -*-

"""
@File       : tasting-monitor.py
@Author     : aura service
@Time       : 2025/5/1 17:18
@Description:

使用方法：
修改env 的值改为抓包小程序 的 user-token
每行一个账号

账号1的tk|是否需要抢券，这里随便填值不为空则表示要抢
账号2的tk|是否需要抢券

示例：
sss113-23129-123123-123123|1
sss234-23129-123123-234312|222


"""
import os
import threading
import time
import requests
import json
from datetime import datetime, timedelta

# 直接跑程序使用的变量
env = """
sss43df3029-7280-4fae-866b-03928825cbbe|1
sssfc2b647d-31c1-46d8-bf76-9e66ba7ae6a6|1
"""

# 青龙面板使用 取消下面注释
# env = os.getenv('tst_tk_env')

debug_mode = False

def log_debug(msg):
    if debug_mode:
        print(f"[debug]{msg}")
    else:
        pass


def checkin(tk):
    import requests
    import json

    url = "https://sss-web.tastientech.com/api/sign/member/signV2"

    payload = {
        "activityId": 59,
        "memberName": "",
        "memberPhone": ""
    }

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf254032b) XWEB/13655",
        'Content-Type': "application/json",
        'version': "3.16.0",
        'xweb_xhr': "1",
        'user-token': tk,
        'channel': "1"
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers)

    log_debug(response.text)
    return response


def api_create_order(tk, activityId=338):
    """
         - 兑换
    :param tk:
    :return:
    """
    url = "https://sss-web.tastientech.com/api/c/pointOrder/create"

    payload = {
        "requestId": "0d4e4367d8c",
        "activityId": activityId
    }

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf254032b) XWEB/13655",
        'Content-Type': "application/json",
        'version': "3.16.0",
        'xweb_xhr': "1",
        'user-token': tk,
        'channel': "1",
        'Sec-Fetch-Site': "cross-site",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Dest': "empty",
        'Accept-Language': "zh-CN,zh;q=0.9",
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    log_debug(response.text)
    return response


def api_get_order_list(tk):
    """
        获取订单列表
    :param tk:
    :return:
    """
    url = "https://sss-web.tastientech.com/api/wx/point/coupon/activity/queryAppletActivityList"

    payload = {
        "platform": "exchangeActivities"
    }

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf254032b) XWEB/13655",
        'Content-Type': "application/json",
        'version': "3.16.0",
        'user-token': tk,
        'channel': "1"
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    log_debug(response.text)
    return response


def get_orders(tk):
    """
        获取订单数据
    :return:
    """
    # 过滤秒杀order
    orders = [i for i in api_get_order_list(tk).json().get("result", []) if
              i.get('groupId') == 41 and i.get('groupName') == '积分秒杀']
    orders = [i for i in orders[0].get('activities', [])]

    re_orders = []
    for order in orders:
        id = order.get('id')
        name = order.get('name')
        exchangePoint = order.get('exchangePoint')
        open_times = [i['openTime'].split('-')[0] for i in order.get('timeActivityInfo', [])]
        re_orders.append({
            "id": id,
            "name": name,
            "exchangePoint": exchangePoint,
            "open_times": open_times
        })
        print(f"{id}|{name}|{exchangePoint}|{open_times}")
    return re_orders


def api_get_my_point(tk):
    url = "https://sss-web.tastientech.com/api/wx/point/myPoint"
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf254032b) XWEB/13655",
        'Content-Type': "application/json",
        'version': "3.16.0",
        'xweb_xhr': "1",
        'user-token': tk,
        'channel': "1",
    }
    response = requests.post(url, data=json.dumps({}), headers=headers)

    print(response.text)
    return response


def monitor_order(tk, order):
    order_id = order.get('id')
    open_times = order.get('open_times', [])
    order_name = order.get('name')

    # 验证 open_times 格式
    valid_open_times = []
    for open_time in open_times:
        try:
            valid_time = datetime.strptime(open_time, "%H:%M").time()
            valid_open_times.append(valid_time)
        except ValueError:
            print(f"无效的时间格式: {open_time}，跳过该时间。")

    if not valid_open_times:
        print(f"没有有效时间，订单 {order_id} 不再监控。")
        return

    now = datetime.now().time()
    in_any_range = any(
        (datetime.combine(datetime.today(), t) - timedelta(minutes=10)).time() <= now <=
        (datetime.combine(datetime.today(), t) + timedelta(minutes=10)).time()
        for t in valid_open_times
    )

    if not in_any_range:
        print(f"当前不在任何 open_time 的 ±10 分钟内，订单 {order_id} 退出监控。")
        return

    print(f"开始监控订单 {order_id} | {order_name}")

    while True:
        now = datetime.now()
        for open_time in valid_open_times:
            target_dt = datetime.combine(now.date(), open_time)
            delta = (target_dt - now).total_seconds()

            if -5 <= delta <= 5:
                # 前后5秒内，每0.5秒调用一次，直到成功或超时
                print(f"进入关键时间区间：{open_time}，开始调用 API 创建订单")
                start_time = time.time()
                while time.time() - start_time <= 10:  # 最多持续10秒（应对系统延迟）
                    try:
                        response = api_create_order(tk, order_id)
                        if response.get("code") == 200:
                            print(f"{tk}|{order_id}|{order_name} 创建成功。")
                            return
                        else:
                            print(f"订单 {order_id} 创建失败: {response.get('message')}")
                    except Exception as e:
                        log_debug(f"调用 API 时发生错误: {e}")
                    time.sleep(0.5)
                log_debug(f"{order_id} 在关键区间内未成功创建，停止尝试。")
                return

            elif -60 <= delta <= 60:
                # 前后1分钟内，每10秒检查一次是否接近目标
                time.sleep(10)
            else:
                # 不在关键时间点前后1分钟内，每30秒检查一次
                time.sleep(30)

        # 若所有时间已过 10 分钟，退出监控
        now = datetime.now()
        if all(
            now > datetime.combine(now.date(), t) + timedelta(minutes=10)
            for t in valid_open_times
        ):
            print(f"所有 open_time 已超过 10 分钟，订单 {order_id} 退出监控。")
            break


# 启动监控进程
def start_monitoring(tks):
    threads = []

    for tk in tks:
        orders = get_orders(tk)
        for order in orders:
            monitor_thread = threading.Thread(target=monitor_order, args=(tk, order,))
            threads.append(monitor_thread)
            monitor_thread.start()

    # 可选：等待所有线程完成
    for thread in threads:
        thread.join()


def filter_lines(input_string):
    # 按行分割字符串
    lines = input_string.splitlines()

    # 过滤空行并检查每行是否包含且仅包含一个 '|'
    filtered_lines = [
        line for line in lines
        if line.strip() and line.count('|') == 1
    ]

    return filtered_lines

def start():
    monitor_tk = []
    print("===== 开始签到 =====")
    for user in filter_lines(env):
        tk, is_monitor = user.split("|")
        print(f"==={tk}")
        # 签到任务
        r = checkin(tk)
        if r.json().get("code") == 200:
            print("签到成功")
        else:
            print(r.json().get("msg", r.text))
        point = api_get_my_point(tk).json().get("result", {}).get('point')
        print(f"积分：{point}")
        if point > 5 and is_monitor:
            monitor_tk.append(tk)
            continue
        else:
            print("积分不足或未设置监控")

    if monitor_tk:
        print("===== 开始监控时间抢0元券 =====")
        start_monitoring(monitor_tk)

if __name__ == '__main__':
    start()
