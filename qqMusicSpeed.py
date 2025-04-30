import requests
import time
import os
import random


ua = "Mozilla/5.0 (Linux; Android 11; M2012K10C Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/90.0.4430.210 Mobile Safari/537.36 MCloudApp/10.0.1"

if __name__ == "__main__":
    QQtoken = 'qqkey'         #从环境变量读取到key#qq音乐cookie，从环境变量获取
    key = os.getenv("QQtoken")
    if not key:
        print(f'⛔️未获取到ck变量：请检查变量 {key} 是否填写')
        exit(0)

def send_request(qq, url, key):
    api_url = f"http://shanhe.kim/api/qy/qyv1.php?qq={qq}&url={encodeURIComponent(url)}&ck={key}&size=4"
    try:
        response = requests.get(api_url, timeout=5)  # 设置超时时间为5秒
        if response.status_code == 200:
            result = {
                "status_code": response.status_code,
                "response_body": response.json()
            }
        else:
            result = {
                "status_code": response.status_code,
                "response_body": response.text
            }
        return result, api_url
    except requests.exceptions.Timeout:
        return {"error": "Request timed out"}, api_url
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, api_url


def encodeURIComponent(string):
    return requests.utils.quote(string)


def log_result(result, api_url, log_file):
    with open(log_file, 'a') as file:
        if "error" in result:
            file.write(f"API URL: {api_url}\n")
            file.write(f"Error: {result['error']}\n")
            print(f"API URL: {api_url}")
            print(f"Error: {result['error']}")
        elif isinstance(result['response_body'], dict):
            file.write(f"Status Code: {result['status_code']}\n")
            file.write(f"Song: {result['response_body'].get('Song', 'N/A')}\n")
            file.write(f"Message: {result['response_body'].get('message', 'N/A')}\n")
            print(f"Status Code: {result['status_code']}")
            print(f"Song: {result['response_body'].get('Song', 'N/A')}")
            print(f"Message: {result['response_body'].get('message', 'N/A')}")
        else:
            file.write(f"API URL: {api_url}\n")
            file.write(f"Status Code: {result['status_code']}\n")
            file.write(f"Response Body: {result['response_body']}\n")
            print(f"API URL: {api_url}")
            print(f"Status Code: {result['status_code']}")
            print(f"Response Body: {result['response_body']}")
        file.write("-" * 50 + "\n")
        print("-" * 50)


if __name__ == "__main__":
    qq = "1478752457"  # 固定的QQ号
    song_links_set = {
        "https://c6.y.qq.com/base/fcgi-bin/u?__=PDcyU4N",
        "https://c6.y.qq.com/base/fcgi-bin/u?__=3iU10lKg0KyF",
        "https://c6.y.qq.com/base/fcgi-bin/u?__=7i9PuX1J1LsA",
        "https://c6.y.qq.com/base/fcgi-bin/u?__=0weSa8gM05dT",
        "https://c6.y.qq.com/base/fcgi-bin/u?__=ddngM0S000RS",
        "https://c6.y.qq.com/base/fcgi-bin/u?__=88bAwMBD05uB",
        "https://c6.y.qq.com/base/fcgi-bin/u?__=SvS3YBJL0iRx",
        "https://c6.y.qq.com/base/fcgi-bin/u?__=eVu8xUUe04pc",
        "https://c6.y.qq.com/base/fcgi-bin/u?__=38fL5Lh",
        "https://c6.y.qq.com/base/fcgi-bin/u?__=iTxmU1K",
        "https://c6.y.qq.com/base/fcgi-bin/u?__=EbJxzCVO1bbs",
        "https://c6.y.qq.com/base/fcgi-bin/u?__=4Ba4Xpz",
        "https://c6.y.qq.com/base/fcgi-bin/u?__=NI1IVfN70TAp",
        "https://c6.y.qq.com/base/fcgi-bin/u?__=6bYGj24g4TdO",
        "https://c6.y.qq.com/base/fcgi-bin/u?__=GQZgc3S10w9b",
        "https://c6.y.qq.com/base/fcgi-bin/u?__=zPEad8Sp0Ja8",
        "https://c6.y.qq.com/base/fcgi-bin/u?__=VGxz87DO0INb",
        "https://c6.y.qq.com/base/fcgi-bin/u?__=I4iU1AED0JvN",
        "https://c6.y.qq.com/base/fcgi-bin/u?__=hW4UAs2A0j6Z",
        "https://c6.y.qq.com/base/fcgi-bin/u?__=BCqQ5Uv10FNv",
        "https://c6.y.qq.com/base/fcgi-bin/u?__=mt5MDQLI0TFj",
        "https://c6.y.qq.com/base/fcgi-bin/u?__=a4xVStAg0AsV",
        "https://c6.y.qq.com/base/fcgi-bin/u?__=p8Cg9fj8esjl",
        "https://c6.y.qq.com/base/fcgi-bin/u?__=AqdZzjDY01Lj",
        "https://c6.y.qq.com/base/fcgi-bin/u?__=0b2yIbPwe0Va",
        "https://c6.y.qq.com/base/fcgi-bin/u?__=tvFsJAeH0ID4",
        "https://c6.y.qq.com/base/fcgi-bin/u?__=z8V97lMv0dh0",
        "https://c6.y.qq.com/base/fcgi-bin/u?__=xny40Ok75xNI"
    }

    max_requests = 20
    count = 0
    log_file = "api_requests.log"

    print(f"开始发送请求，总共{max_requests}次，每次间隔180到300秒之间...")

    while count < max_requests:
        url = random.choice(list(song_links_set))
        api_url = f"https://shanhe.kim/api/qy/qyv1.php?qq={qq}&url={encodeURIComponent(url)}&ck={key}&size=4"
        print(f"Sending request {count + 1} to {api_url}")
        result, _ = send_request(qq, url, key)
        log_result(result, api_url, log_file)
        count += 1
        if count < max_requests:
            sleep_time = random.randint(180, 300)  # 生成180到300秒之间的随机数
            print(f"等待 {sleep_time} 秒后继续...")
            time.sleep(sleep_time)  # 等待随机时间

    print("所有请求已完成。")
