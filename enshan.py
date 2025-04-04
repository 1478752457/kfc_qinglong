import os
import re
import requests

# 读取环境变量
enshanck = os.getenv("enshanck")
plustoken = os.getenv("plustoken")

def push(contents):
    """推送消息到推送加"""
    headers = {'Content-Type': 'application/json'}
    json_data = {
        "token": plustoken,
        'title': '恩山签到',
        'content': contents.replace('\n', '<br>'),
        "template": "json"
    }
    resp = requests.post('http://www.pushplus.plus/send', json=json_data, headers=headers).json()
    print('push+推送成功' if resp['code'] == 200 else f'push+推送失败: {resp.get("msg", "未知错误")}')

def get_credit_info(cookie):
    """获取积分和恩山币信息"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36",
        "Cookie": cookie,
    }
    url = 'https://www.right.com.cn/FORUM/home.php?mod=spacecp&ac=credit&showcredit=1'
    response = requests.get(url, headers=headers)

    try:
        coin = re.findall(r"恩山币: </em>(.*?)&nbsp;", response.text)[0].strip()
        point = re.findall(r"<em>积分: </em>(.*?)<span", response.text)[0].strip()
        return f"恩山币：{coin}\n积分：{point}"
    except IndexError as e:
        return f"未能找到匹配的积分或恩山币信息: {str(e)}"
    except Exception as e:
        return f"请求或解析网页内容时发生错误: {str(e)}"

def main():
    if not enshanck or not plustoken:
        print("请检查是否已正确设置环境变量 enshanck 和 plustoken")
        return

    result = get_credit_info(enshanck)
    print(result)
    push(contents=result)

if __name__ == "__main__":
    main()