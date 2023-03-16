import sys
import ntchat
import xml.dom.minidom
import re
import pymysql
import uuid

welcome = '欢迎使用小助手!'
contact_help = "若您需要发送消息，您可以采用\n(匿名/不匿名)to(:)楼号-房号【空格或换行】通话内容\n形式向您想对话的对象发送信息,默认发送方式为匿名\n"
key_list = ['帮助','如何发送','住户列表','关键词']
success = '发送成功'
send_fail = '请求失败，发送格式错误或未找到对应微信id'
mass_fail = '您不是管理员，不可群发'
wechat = ntchat.WeChat()
MSG_TO_ALL = 0
MSG_TO_NONE = -1
MSG_TYPE = { "ERROR_MSG": -1,#信息错误，无法识别
           "ANONYMOUS_MSG": 1,
           "IDENTIFIABLE_MSG": 2,
           "MASS_MSG": 3,#群发请求
           "HELP_MSG": 4,#请求帮助
           "SEARCH_MSG": 5,#查看住户列表请求
           "ALL_KEY":6,#查看所有关键词
           }
MSG_CON_TYPE = { "TEXT":1,#文本
                "IMG":2,#图片
                "USER_CARD":3,
                "LINK_CARD":4,
                "FILE":5,
                "VIDEO":6,
                "GIF":7}

# 新好友请求通知
@wechat.msg_register(ntchat.MT_RECV_FRIEND_MSG)
def on_recv_add_msg(wechat_instance: ntchat.WeChat, message):
    xml_content = message["data"]["raw_msg"]
    dom = xml.dom.minidom.parseString(xml_content)

    # 从xml取相关参数
    fromuserID = dom.documentElement.getAttribute("fromusername")#获取微信id
    content = dom.documentElement.getAttribute("content")#获取验证信息
    alias = dom.documentElement.getAttribute("alias")#获取微信号
    #可设置小区(8-401)内or多个小区(xx小区-8-401)
    pattern = r'\d-\d'

    # judge = re.match( r'\d-\d', content) is not None
    # print(judge)

    #判断content是否符合验证信息格式
    if re.match( pattern, content) is not None:
    # if judge:#非空则匹配成功
        print("匹配成功,格式正确")
        data = re.findall("(.*)-(.*)", content)[0]  # data为元组格式('8','401')

        #判断数据库里有没有这个人
        building = data[0]
        room = data[-1]
        print(f'微信号为{fromuserID},房号为{room},楼号为{building}')
        judge = search_user_byPos(building,room)

        if judge == 0:#这个地方还没人住
            #或许是同意申请必须的？
            encryptusername = dom.documentElement.getAttribute("encryptusername")#获取加密用户名？
            ticket = dom.documentElement.getAttribute("ticket")#？
            scene = dom.documentElement.getAttribute("scene")#？
            # 自动同意好友申请
            wechat_instance.accept_friend_request(encryptusername, ticket, int(scene))
            #用户信息存入数据库**（wait）
            insert_user(fromuserID,alias,data)
            #发送欢迎
            send_welcome(fromuserID)
        else:#管理员手动修改并添加
            #加入到待处理的表中
            print(f"数据库中已存在{building}-{room}")
    else:
        print("未匹配成功，验证信息",content)

# 接受到好友text消息
@wechat.msg_register(ntchat.MT_RECV_TEXT_MSG)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    data = message["data"]
    from_wxid = data["from_wxid"]
    self_wxid = wechat_instance.get_login_info()["wxid"]

    # 判断消息不是自己发的，并回复对方
    if from_wxid != self_wxid:
        # 类型判断，初步处理
        msg_raw = data['msg']
        result = judge_msg(msg_raw)
        print("result:",result)
        type_msg = result[0]
        print("type_msg:",type_msg)
        content_msg = result[1]
        print("content_msg:",content_msg)
        #分类处理
        if type_msg == MSG_TYPE["ANONYMOUS_MSG"] or type_msg == MSG_TYPE["IDENTIFIABLE_MSG"]:
        # 查找数据库，找到block=8,room=501对应的wxid
            msg_handle = handle_contact_msg(content_msg)
            print("msg_handle:\n", msg_handle)
            if msg_handle[0]:
                user = msg_handle[1]
                to_wxid = user['to_id']
                content = user['content']
                print("to_wxid:\n",to_wxid)
                if to_wxid and type_msg == MSG_TYPE["ANONYMOUS_MSG"]:#匿名发送
                    wechat_instance.send_text(to_wxid=to_wxid, content=f"有人给你发送了一条消息: { content }")
                    insert_message(MSG_TYPE["ANONYMOUS_MSG"],from_wxid,to_wxid,MSG_CON_TYPE["TEXT"],content)
                    send_success(from_wxid)
                elif to_wxid and type_msg == MSG_TYPE["IDENTIFIABLE_MSG"]:#不匿名发送
                    #寻找发送者住址
                    building,room = search_user_byid(from_wxid)
                    wechat_instance.send_text(to_wxid=to_wxid, content=f"{building}-{room}给你发送了一条消息: \n{ content }")
                    insert_message(MSG_TYPE["IDENTIFIABLE_MSG"],from_wxid,to_wxid,MSG_CON_TYPE["TEXT"],content)
                    send_success(from_wxid)
            else:
                send_fail(from_wxid)
        elif type_msg == MSG_TYPE["MASS_MSG"]:#群发,仅管理员 "群发【\n或空格】发送帮助"
            is_server = judge_server()
            if is_server[0] == False:
                print(f"{from_wxid}不是管理员,不可群发")
                mass_send_fail(from_wxid)
            else:#是管理员
                server = is_server[1]
                authority = server['authority']#暂时未使用该属性
                if content_msg == "发送帮助":
                    # #获取联系人列表
                    contacts = wechat.get_contacts()
                    for user in contacts:
                        wx_id = user['wxid']
                        print(f"向{wx_id}发送帮助")
                        send_help(wx_id)
                elif content_msg == "发送欢迎":
                    contacts = wechat.get_contacts()
                    for user in contacts:
                        wx_id = user['wxid']
                        print(f"向{wx_id}发送欢迎")
                        send_welcome(wx_id)
                else:
                    contacts = wechat.get_contacts()
                    for user in contacts:
                        wx_id = user['wxid']
                        print(f"向{wx_id}发送{content_msg}")
                        wechat_instance.send_text(to_wxid=wx_id,content=content_msg)
                insert_message(MSG_TYPE["MASS_MSG"],from_wxid,MSG_TO_ALL,MSG_CON_TYPE["TEXT"],content_msg)
        elif type_msg == MSG_TYPE["HELP_MSG"]:#“帮助”关键词
            send_help(from_wxid)
            insert_message(MSG_TYPE["HELP_MSG"],from_wxid,MSG_TO_NONE,MSG_CON_TYPE["TEXT"],content_msg)
        elif type_msg == MSG_TYPE["SEARCH_MSG"]:#“住户列表”关键词
            send_located_list(from_wxid)
            insert_message(MSG_TYPE["SEARCH_MSG"],from_wxid,MSG_TO_NONE,MSG_CON_TYPE["TEXT"],content_msg)
        elif type_msg == MSG_TYPE["ALL_KEY"]:#查看所有关键词
            send_key_list(from_wxid)
            insert_message(MSG_TYPE["ALL_KEY"],from_wxid,MSG_TO_NONE,MSG_CON_TYPE["TEXT"],content_msg)
        elif type_msg == MSG_TYPE["ERROR_MSG"]:#请求失败
            send_fail(from_wxid)
        else:
            print("type_msg未匹配")
            send_fail(from_wxid)

#群发msg
def send_toall(msg):
    contacts = wechat.get_contacts()
    for user in contacts:
        wx_id = user['wxid']
        # print(f"向{wx_id}发送帮助")
        # if wx_id == filehelper:
        wechat.send_text(to_wxid=wx_id, content=msg)
                    

# 发送欢迎信息
def send_welcome(wxid):
    if wxid:
        wechat.send_text(to_wxid=wxid, content=welcome)

# 发送帮助信息
def send_help(wxid):
    key_help = "可使用关键词包括:\n"+" ".join(key_list)
    split_img = "==================\n"
    help_msg = "1."+contact_help+split_img+"2.您也可以直接使用关键词查询，"+key_help
    if wxid:
        wechat.send_text(to_wxid=wxid, content=help_msg)

# 发送成功提示
def send_success(wxid):
    if wxid:
        wechat.send_text(to_wxid=wxid, content=success)

#发送失败提示
def send_fail(wxid):
    if wxid:
        wechat.send_text(to_wxid=wxid, content=send_fail)

def mass_send_fail(wxid):
    if wxid:
        wechat.send_text(to_wxid=wxid, content=mass_fail)

#发送已入住列表
def send_located_list(wxid):
    list_pos = search_located_pos()
    msg = "当前已登记房间为:\n"+" ".join(list_pos)
    if wxid:
        wechat.send_text(to_wxid=wxid, content=msg)

#发送关键词列表
def send_key_list(wxid):
    msg = "可使用关键词包括:\n"+" ".join(key_list)
    if wxid:
        wechat.send_text(to_wxid=wxid, content=msg)

#分类收到的类型
def judge_msg(data):
    ret_type = -1
    ret_content = ""
    #1:匿名信息;2.不匿名信息；3.其他信息
    is_send = judge_send(data)
    if is_send[0] >= 1 :#如果为通讯,(type,content)
        ret_type = is_send[0]
        ret_content = is_send[1]
        return ret_type,ret_content
    is_mass = judge_mass(data)
    if is_mass[0] == MSG_TYPE["MASS_MSG"]:# 是群发消息
        ret_type = is_mass[0] #类型标记为群发消息
        ret_content = is_mass[1] # 群发内容
    else:#关键词查找
        ret_type = judge_word(data) # 3帮助; 5住户列表; -1不匹配
        ret_content = data
    return ret_type,ret_content

#判断是否为通讯及类型
def judge_send(data):#返回(type,content)
    msg = data
    split_list = msg.split('to:', 1)  # 以空格为分隔符，分割成两个部分
    type_send = split_list[0]
    result_type = -1
    result_content = ""
    if len(split_list) <= 1:#以防：为中文字符
        split_list = msg.split('to：', 1)
        type_send = split_list[0]
    if len(split_list) <= 1:#以防未输入：
        split_list = msg.split('to', 1)
        type_send = split_list[0]
    if len(split_list) <= 1:#不是发消息
        return result_type,result_content
    if type_send == "匿名":
        print(f"1:type = {type_send},list = {split_list[1]}")
        result_type = MSG_TYPE["ANONYMOUS_MSG"]
        result_content =split_list[1]
    elif type_send == "不匿名":
        print(f"2:type = {type_send},list = {split_list[1]}")
        result_type = MSG_TYPE["IDENTIFIABLE_MSG"]
        result_content =split_list[1]
    else:#默认匿名
        print(f"3:type = {type_send},list = {split_list}")
        result_type = MSG_TYPE["ANONYMOUS_MSG"]
        result_content = split_list[1]
        print("result_content:",result_content)
    return result_type,result_content

#判断是否为关键字查询
def judge_word(data):
    ret_type = -1
    help_word = ['帮助','如何发送']
    search_word = ['住户列表']
    key_word = ['关键词']
    if data in help_word:
        ret_type = MSG_TYPE["HELP_MSG"]
    elif data in search_word:
        ret_type = MSG_TYPE["SEARCH_MSG"]
    elif data in key_word:
        ret_type = MSG_TYPE["ALL_KEY"]
    else:
        ret_type = MSG_TYPE["ERROR_MSG"]
    return ret_type

#判断是否为群发消息
def judge_mass(data):
    split_list = data.split(' ',1)#“群发【换行或空格】群发内容”
    type_mass = split_list[0]
    data_type = -1
    content = ""
    if len(split_list) <= 1:#以防：为中文字符
        split_list = data.split('\n', 1)
        type_mass = split_list[0]
    if type_mass == "群发":
        content = split_list[1]
        data_type = MSG_TYPE["MASS_MSG"]
    else:
        data_type = -1
    return data_type,content

#判断是否为管理员
def judge_server(wx_id):
    print(f"查找微信id为{wx_id}的管理员")
    search_user = "SELECT * FROM server WHERE wx_id = %s";
    cursor.execute(search_user,wx_id)
    userList = cursor.fetchall()
    list_len = len(userList)
    if list_len > 1 or list_len == 0:
        print(f"找到的微信id有{list_len}个")
        return False,list_len
    else:
        #寻找发送者
        server = userList[0]
        print(f"是管理员,权限为{server['authority']}")
        return True,server
    

# 处理通讯消息
def handle_contact_msg(data):
    msg = data
    print("msg:",msg)
    split_list = msg.split(' ', 1)  # 以空格为分隔符，分割成两个部分
    if len(split_list) <= 1:
        split_list = msg.split('\n', 1)  # 以空格为分隔符，分割成两个部分
    to_position = split_list[0]  # 获取房间号8-401
    content = split_list[1]  # 获取空格后面的部分
    pattern = r'\d-\d'
    result = True
    #判断content是否符合验证信息格式
    if re.match( pattern, to_position) is not None:
        print("匹配成功,格式正确")
        result = True
        data = re.findall("(.*)-(.*)", to_position)[0]  # data为元组格式('8','401')
        building = data[0]  # 获取楼号'8'
        room = data[-1]  # 获取房号'401'
        to_wxid = search_user_byPos(building,room)
        result_dict = {'to_id': to_wxid, 'content': content,'building': building,'room':room}  # 存储为字典
    else:
        result = False
        print("匹配不成功")
      # 获取冒号后面的部分
    return result,result_dict

#插入数据库
def insert_user(wxid,wx_name,data):
    building = data[0]  # 获取楼号'8'
    room = data[-1]  # 获取房号'401'
    print(f'微信号为{wxid},房号为{room},楼号为{building}')
    # insert_sql = "insert into server(wx_id,wx_name,authority) values(%(wxid)s,%(name)s,%(authority)s)"
    insert_user = "insert into user(wx_id,wx_name,building,room) values(%(id)s,%(name)s,%(building)s,%(room)s)"
    data = {
        "id": wxid,
        "name": wx_name,
        "building": building,
        "room": room}
    print(data)
    cursor.execute(insert_user, data)
    conn.commit()
    print("插入user成功")

def insert_message(msg_type,from_id,to_id,cont_type,content):
    print(f"从{from_id}向{to_id}发送类型为{msg_type}的内容:{content},内容类型为{cont_type}")
    mid = uuid.uuid1()
    insert_message = "insert into message(mid,msg_type,from_id,to_id,cont_type,content) values(%s,%s,%s,%s,%s,%s)"
    params = (mid,msg_type,from_id,to_id,cont_type,content)
    #
    cursor.execute(insert_message,params)
    conn.commit()
    print("插入message成功")
    
#查找用户
def search_user_all(situation):
    search_sql = "SELECT * FROM user "+situation
    print("search sql:",search_sql)
    cursor.execute(search_sql)
    userList = cursor.fetchall()
    return userList

def search_user_byPos(building,room):
    print(f'查找房号为{room},楼号为{building}的用户\n')
    search_to_user = "SELECT * FROM user WHERE room = %s AND building = %s";
    params1 = (room,building)
    cursor.execute(search_to_user,params1)
    userList = cursor.fetchall()
    list_len = len(userList)
    if list_len > 1:
        print(f"找到的微信id个数大于1")
        return userList
    elif list_len == 0:
        print(f"找到的微信id个数为0")
        return 0
    else:
        to_id = userList[0]['wx_id']
        print(f"找到的微信id为{to_id}")
        return to_id

def search_user_byid(from_id):
    print(f"查找微信id为{from_id}的房间与楼号")
    search_user = "SELECT * FROM user WHERE wx_id = %s";
    cursor.execute(search_user,from_id)
    userList = cursor.fetchall()
    list_len = len(userList)
    if list_len > 1 or list_len == 0:
        print(f"找到的微信id有{list_len}个")
        return None
    else:
        #寻找发送者
        building = userList[0]['building']
        room = userList[0]['room']
        print(f"找到的房间号为{room},楼号为{building}")
        return building,room

def search_located_pos():
    userList = search_user_all("order by building")
    print("userList:",userList)
    posList = []
    for user in userList:
        b = user['building']
        r = user['room']
        result = f"{b}-{r}"
        posList.append(result) #以8-401形式显示
    print("posList:",posList)
    return posList


'''
从数据库初始化数据
如：欢迎语/菜单/...
（待定）机器人wxid匹配
'''
def initData():
    pass


# 打开pc微信, smart: 是否管理已经登录的微信
wechat.open(smart=True)

# 等待登录
wechat.wait_login()


# 连接mysql
conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='123456',charset='utf8',db='communitydb')
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

# # 获取群列表
# rooms = wechat.get_rooms()


#调试
#关闭连接
cursor.close()
conn.close()
ntchat.exit_()
sys.exit()

#运行
# try:
#     while True:
#         pass
# except KeyboardInterrupt:
#     #关闭连接
#     cursor.close()
#     conn.close()
#     # 退出微信
#     ntchat.exit_()
#     sys.exit()
