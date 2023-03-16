import sys
import ntchat
from utils import logger

log = logger.get_logger("DemoInstance")

wechat = ntchat.WeChat()
wechat.open(smart=True)
lgInfo = wechat.get_login_info()

log.debug("communicate wechat pid: %d", wechat.pid)
# wechat.send_text(to_wxid="filehelper",content="hello")


{
    'data': 
        {  
            'at_user_list': [],
            'from_wxid': 'wxid_zldk8ioij82c22',
            'is_pc': 0,
            'msg': '你好',
            'msgid': '1039827569261394861', 
            'room_wxid': '', 
            'timestamp': 1677210214, 
            'to_wxid': 'wxid_y72ubiy0n2pq22', 
            'wx_type': 1
        }, 
    'type': 11046
}
{'data': 
    {'from_wxid': 'fmessage', 
    'is_pc': 0, 
    'msgid': '3128120412711003067', 
    'raw_msg': 
    '', 
    
    'room_wxid': '', 
    'timestamp': 1677244888, 
    'to_wxid': 'wxid_y72ubiy0n2pq22', 
    'wx_type': 37}, 
    'type': 11049}   
<msg fromusername="wxid_zldk8ioij82c22" 
    encryptusername="v3_020b3826fd030100000000008a8924b4756cb2000000501ea9a3dba12f95f6b60a0536a1adb64928e7bd17b66d8a5e54570f71222865b7c75504c65652e8bbfc0e30c77db4d8f7527bda93d4cf826225985bcccb55a0b0dc217943c5876a77447a1d17@stranger" 
    fromnickname="yy" 
    content="我是yy" 
    fullpy="yy" 
    shortpy="YY" 
    imagestatus="3" 
    scene="6" 
    country="CN" 
    province="Zhejiang" 
    city="Wenzhou" 
    sign="" 
    percard="1" 
    sex="2" 
    alias="yyowo111" 
    weibo="" 
    albumflag="0" 
    albumstyle="0" 
    albumbgimgid="" 
    snsflag="273" 
    snsbgimgid="http://mmsns.qpic.cn/mmsns/PiajxSqBRaEIxQVyknaN1lrYsrqdp9xIcnUWibdibiapP6f9mHB3TpVq2x8FY45q88aX/0" 
    snsbgobjectid="11679807551720468535" 
    mhash="1dfc001a2a85094578ac069480175133" 
    mfullhash="1dfc001a2a85094578ac069480175133" 
    bigheadimgurl="http://wx.qlogo.cn/mmhead/ver_1/eUnHiaegCiaVbpic18mA6ziacmWIomBqhAVIKW3uhPsiayHPrziaX34TnjYCZTMKJaV3iaQnaguFfibxE8Mhv0LibuicYILMPpia2bHTiacXCGQTlibfGmE0/0" 
    smallheadimgurl="http://wx.qlogo.cn/mmhead/ver_1/eUnHiaegCiaVbpic18mA6ziacmWIomBqhAVIKW3uhPsiayHPrziaX34TnjYCZTMKJaV3iaQnaguFfibxE8Mhv0LibuicYILMPpia2bHTiacXCGQTlibfGmE0/96" 
    ticket="v4_000b708f0b04000001000000000025c15b2418d52d798717d7b9f8631000000050ded0b020927e3c97896a09d47e6e9e91bfe260ddde0c220503b25f6e8097f1d26e95f6616c445015d5c3bdd59db9ccb0c4bdf535e33cfbc2411573e3d905ea88a34212b9b6d7176506c765e2c6221266d30a7d3cc0ee48c7d5e2ec1f6197abaf57a5d807a4527f39352d26e8981872cc65443dd24016b3e4@stranger" 
    opcode="2" 
    googlecontact="" 
    qrticket="" 
    chatroomusername="" 
    sourceusername="" 
    sourcenickname="" 
    sharecardusername="" 
    sharecardnickname="" 
    cardversion="" 
    extflag="0">
    <brandlist count="0" ver="810590174">
    </brandlist>
    </msg>     
xml_content:%s <msg fromusername="wxid_zldk8ioij82c22" encryptusername="v3_020b3826fd030100000000008a8924b4756cb2000000501ea9a3dba12f95f6b60a0536a1adb64928e7bd17b66d8a5e54570f71222865b7c75504c65652e8bbfc0e30c77db4d8f7527bda93d4cf826225985bcccb55a0b0dc217943c5876a77447a1d17@stranger" fromnickname="yy" content="我是yy" fullpy="yy" shortpy="YY" imagestatus="3" scene="6" country="CN" province="Zhejiang" city="Wenzhou" sign="" percard="1" sex="2" alias="yyowo111" weibo="" albumflag="0" albumstyle="0" albumbgimgid="" snsflag="273" snsbgimgid="http://mmsns.qpic.cn/mmsns/PiajxSqBRaEIxQVyknaN1lrYsrqdp9xIcnUWibdibiapP6f9mHB3TpVq2x8FY45q88aX/0" snsbgobjectid="11679807551720468535" mhash="1dfc001a2a85094578ac069480175133" mfullhash="1dfc001a2a85094578ac069480175133" bigheadimgurl="http://wx.qlogo.cn/mmhead/ver_1/eUnHiaegCiaVbpic18mA6ziacmWIomBqhAVIKW3uhPsiayHPrziaX34TnjYCZTMKJaV3iaQnaguFfibxE8Mhv0LibuicYILMPpia2bHTiacXCGQTlibfGmE0/0"43dd24016b3e4@stranger" opcode="2" googlecontact="" qrticket="" chatroomusername="" sourceusername="" sourcenickname="" sharecardusername="" sharecardnickname="" cardversion="" extflag="0"><brandlist count="0" ver="810590174"></brandlist></msg>