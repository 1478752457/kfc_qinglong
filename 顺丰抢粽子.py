import hashlib
import json
import os
import time
from datetime import datetime
from urllib.parse import unquote
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class SFExpress:
    def __init__(self, info, index):
        split_info = info.split('@')
        url = split_info[0]
        self.index = index + 1
        print(f"\n{'='*20} 🔄 开始执行第{self.index}个账号 🔄 {'='*20}")
        
        self.s = requests.session()
        self.s.verify = False
        self.headers = {
            'Host': 'mcs-mimp-web.sf-express.com',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090551) XWEB/6945 Flue',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'zh-CN,zh',
            'platform': 'MINI_PROGRAM',
        }
        
        self.login_res = self.login(url)
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.session_id = None
        self.cookies = None  # 新增：保存完整cookies

    def login(self, sfurl):
        try:
            decoded_url = unquote(sfurl)
            response = self.s.get(decoded_url, headers=self.headers)
            
            print("\n=== 登录调试信息 ===")
            #print("Cookies:", self.s.cookies.get_dict())
            
            self.cookies = self.s.cookies.get_dict()  # 保存完整cookies
            self.phone = self.cookies.get('_login_mobile_', '')
            self.mobile = self.phone[:3] + "*" * 4 + self.phone[7:] if self.phone else ''
            self.session_id = self.cookies.get('sessionId')
            
            if self.phone and self.session_id:
                print(f'👤 用户:【{self.mobile}】登陆成功')
                print(f'🔑 sessionId: {self.session_id}')
                return True
            
            print('❌ 登录失败')
            return False
        except Exception as e:
            print(f'❌ 登录异常: {str(e)}')
            return False

    def getSign(self):
        timestamp = str(int(time.time() * 1000))
        token = 'wwesldfs29aniversaryvdld29'
        sysCode = 'MCS-MIMP-CORE'
        data = f'token={token}&timestamp={timestamp}&sysCode={sysCode}'
        signature = hashlib.md5(data.encode()).hexdigest()
        self.headers.update({
            'sysCode': sysCode,
            'timestamp': timestamp,
            'signature': signature
        })

    def do_request(self, url, data={}, req_type='post'):
        self.getSign()
        try:
            if req_type.lower() == 'get':
                response = self.s.get(url, headers=self.headers)
            else:
                response = self.s.post(url, headers=self.headers, json=data)
            
            # 每次请求后更新cookies
            self.cookies = self.s.cookies.get_dict()
            self.session_id = self.cookies.get('sessionId', self.session_id)
            
            return response.json()
        except Exception as e:
            print(f'请求异常: {str(e)}')
            return None

    def sign(self):
        print('🎯 开始执行签到')
        json_data = {"comeFrom": "vioin", "channelFrom": "WEIXIN"}
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~integralTaskSignPlusService~automaticSignFetchPackage'
        response = self.do_request(url, data=json_data)
        
        if response and response.get('success'):
            count_day = response.get('obj', {}).get('countDay', 0)
            if response.get('obj') and response['obj'].get('integralTaskSignPackageVOList'):
                packet_name = response["obj"]["integralTaskSignPackageVOList"][0]["packetName"]
                print(f'✨ 签到成功，获得【{packet_name}】，本周累计签到【{count_day + 1}】天')
            else:
                print(f'📝 今日已签到，本周累计签到【{count_day + 1}】天')
        else:
            print(f'❌ 签到失败: {response.get("errorMessage") if response else "无响应"}')

    def exchange_goods(self, goods_info, address_info=None):
        """兑换商品方法（修正商品名称显示问题）
        
        Args:
            goods_info: 商品信息，可以是元组(ID, 名称)或字符串ID
            address_info: 可选地址信息
        """
        if not self.session_id:
            print("❌ 无法获取sessionId，兑换失败")
            return False
            
        # 解析商品信息
        if isinstance(goods_info, tuple) and len(goods_info) == 2:
            goods_id, goods_name = goods_info
        else:
            goods_id = goods_info
            goods_name = f'商品(ID:{goods_id})'

        print(f'🎁 开始兑换商品: {goods_name}')
        
        # 请求头设置
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "syscode": "MCS-MIMP-CORE",
            "accept": "application/json, text/plain, */*",
            "cookie": f"sessionId={self.session_id}; " + "; ".join(
                [f"{k}={v}" for k,v in self.cookies.items()]
            ),
        }
        
        # 请求体设置
        payload = {
            "from": "Point_Mall",
            "orderSource": "POINT_MALL_EXCHANGE",
            "goodsNo": goods_id,
            "quantity": 1,
            "province": "广东省",  # 省
            "city": "广州市",     # 市
            "distinct": "荔湾区", # 区镇
            "receiveContact": "吕布",  # 收货名字
            "receiveAddress": "东漖街芳和花园18栋503",  # 详细地址
            "receivePhone": "13544438454",  # 收货人手机号
            "fullReceiveAddress": "广东省广州市荔湾区东漖街芳和花园18栋503"  # 完整地址
        }
        
        url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberGoods~pointMallService~createOrder"
        
        try:
            response = self.s.post(url, headers=headers, json=payload)
            response_data = response.json()
            
            if response_data.get('success'):
                print(f'🎉 兑换成功: {goods_name} 订单号:{response_data.get("obj",{}).get("orderNo","")}')
                return True
            else:
                print(f'❌ {goods_name} 兑换失败: {response_data.get("errorMessage", "未知错误")}')
                return False
        except Exception as e:
            print(f'❌ {goods_name} 兑换请求异常: {str(e)}')
            return False

    def main(self):
        """主执行流程"""
        if not self.login_res: 
            return False
        
        print('\n' + '='*30 + '🚚 顺丰速运 开始执行 🚚' + '='*30)
        self.sign()
        
        # 商品列表（ID + 名称）
        goods_list = [
            ('GOODS20250507165644960', '粽力前行礼盒'),  # 端午粽子礼盒
            ('GOODS20250507165051296', '乐在途粽礼包')   # 端午旅行粽子套装
        ]
        
        for goods_info in goods_list:
            print(f'\n🛒 尝试兑换商品: {goods_info[1]}(ID:{goods_info[0]})')
            success = self.exchange_goods(goods_info)
            if success:
                print(f'✅ 成功兑换 {goods_info[1]}')
            time.sleep(1)
        
        print('\n' + '='*30 + '🚚 顺丰速运 执行完毕 🚚' + '='*30)
        return True
        
if __name__ == '__main__':
    tokens = os.getenv('sfsyUrl', '').split('&')
    print(f"\n{'='*30} 🚚 共获取到{len(tokens)}个账号 🚚 {'='*30}")
    
    for index, infos in enumerate(tokens):
        SFExpress(infos, index).main()