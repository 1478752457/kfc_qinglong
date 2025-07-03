// 自定义设置定时发送wanip到wxpusher需要自己填写WP_APP_TOKEN_ONE，
// process.env.WP_APP_TOKEN_wxuid 。用于发送ip通知的代码，用于青龙面板，代码思考与记录。node.js的get和post使用分享。其他通知平台可参考修改，用了几天稳定好用，注释全面，适合小白对相关代码的理解。



const http = require('http');
const timeout = 10000; //超时时间(单位毫秒)
let wxuid="";//也可以直接写到这里 或者在cofing文件里赋值。export process.env.WP_APP_TOKEN_wxuid =
let WP_APP_TOKEN_ONE = "";//也可以直接写到这里 或者才cofing文件里赋值。export WP_APP_TOKEN_ONE  =
if (process.env.WP_APP_TOKEN_ONE) {
    WP_APP_TOKEN_ONE = process.env.WP_APP_TOKEN_ONE;
}
console.log("wx通知ID:"+WP_APP_TOKEN_ONE);
if (process.env.WP_APP_TOKEN_wxuid) {
    wxuid== process.env.WP_APP_TOKEN_wxuid;
}

arIpAddress();//主程序

//处理ip 方便操作
function sendmessip(ip) {
        // url= 'http://wxpusher.zjiecode.com/api/send/message';
        console.log("获得的ip:"+ip);
        let vhtml=ipshows(ip);
        wxpusherNotifyByOne("每日ip推送",vhtml,"");
}

function ipshows(ip){ //这里定义需要的其他内网地址。
    let ipshow='<br\><a href="http://'+ip+':801">路由器管理地址：http://'+ip+':801</a>';
    ipshow=ipshow+'<br\><a href="http://'+ip+':802">青龙地址：http://'+ip+':802</a>';
    ipshow=ipshow+'<br\><a href="http://'+ip+':803">华硕地址：http://'+ip+':803</a>';
    ipshow=ipshow+'<br\><a href="http://'+ip+':804">小钢炮地址：http://'+ip+':804</a>';
    return ipshow;
}

// 获得外网地址
async  function arIpAddress() {
   let rawData = '';
   let error;
   let ip;
   http.get('http://ifconfig.co', {"timeout":timeout},(res) => {
     const { statusCode } = res;
     const contentType = res.headers['content-type'];
  // 任何 2xx 状态码都表示成功响应，但这里只检查 200。
  if (statusCode !== 200) {
    error = new Error('Request Failed.\n' +
                      `Status Code: ${statusCode}`);
  }
  if (error) {
    console.error(error.message);
    // 消费响应数据以释放内存
    res.resume();
    return;
  }
res.setEncoding('utf8');
res.on('data', (chunk) => { rawData += chunk; });
res.on('end', () => {
    try {
      const parsedData = rawData;
      console.log("获得的页面成功")
      kk=parsedData;
      i=kk.indexOf('class="ip">');
      ie=kk.indexOf("</code></p>");
      ip=kk.substring(i+11,ie);
      console.log("获得IP地址成功:" + ip + "!");
      sendmessip(ip) ;
      }
      catch (e) {
      console.error(e.message);
      }
  });
}).on('error', (e) => {
  console.error(`Got error: ${e.message}`);
});
}

function wxpusherNotifyByOne(text, desp, strsummary = "") {
    return new Promise((resolve) => {
        if (WP_APP_TOKEN_ONE) {
            var WPURL = "";
            if (strsummary) {
                strsummary = text + "\n" + strsummary;
            } else {
                strsummary = text + "\n" + desp;
            }

            if (strsummary.length > 96) {
                strsummary = strsummary.substring(0, 95) + "...";
            }
            let uids =wxuid;
            desp = `<section style="width: 24rem; max-width: 100%;border:none;border-style:none;margin:2.5rem auto;" id="shifu_imi_57" donone="shifuMouseDownPayStyle('shifu_imi_57')">
    <section
        style="margin: 0px auto;text-align: left;border: 2px solid #212122;padding: 10px 0px;box-sizing:border-box; width: 100%; display:inline-block;"
        class="ipaiban-bc">
        <section style="margin-top: 1rem; float: left; margin-left: 1rem; margin-left: 1rem; font-size: 1.3rem; font-weight: bold;">
            <p style="margin: 0; color: black">`+
                text+`
            </p>
        </section>
        <section style="display: block;width: 0;height: 0;clear: both;"></section>
        <section
            style="margin-top:20px; display: inline-block; border-bottom: 1px solid #212122; padding: 4px 20px; box-sizing:border-box;"
            class="ipaiban-bbc">
            <section
                style="width:25px; height:25px; border-radius:50%; background-color:#212122;display:inline-block;line-height: 25px"
                class="ipaiban-bg">
                <p style="text-align:center;font-weight:1000;margin:0">
                    <span style="color: #ffffff;font-size:20px;">&#128226;</span>
                </p>
            </section>
            <section style="display:inline-block;padding-left:10px;vertical-align: top;box-sizing:border-box;">
            </section>
        </section>
        <section style="margin-top:0rem;padding: 0.8rem;box-sizing:border-box;">
            <p style=" line-height: 1.6rem; font-size: 1.1rem; ">
                `+desp+`
                        </p>            
        </section>
    </section>
</section>`;

           const body = {
                "appToken": WP_APP_TOKEN_ONE,
                "content":  desp ,
                "summary": strsummary,
                "contentType": 2,
                "topicIds":[],
                "uids":[uids],
                "url": "http://wxpusher.zjiecode.com/api/send/message"
            };
            const bodyjson= JSON.stringify(body);
            const options = {
                hostname: 'wxpusher.zjiecode.com',
                path: '/api/send/message',
                method: 'post',
                headers: {"Content-Type": "application/json",},
                timeout:timeout
            };
             console.log(options);
             const req = http.request(options, (res) => {
                res.setEncoding('utf8');
                res.on('data', (chunk) => {
                  data = JSON.parse(chunk);
                  if (data.code === 1000) {
                     console.log("WxPusher 发送通知消息成功!\n");
                     for(let k in data){
                     console.log(""+k+":"+data[k])}
                  }
                 });
                 req.on('error', (e) => {
                 console.error(`problem with request: ${e.message}`);
                 console.log("WxPusher 发送通知调用 API 失败！！\n"+ e);
               });

               });
               // 请求body。
             req.write(bodyjson);
             req.end();
        }
    });
}
