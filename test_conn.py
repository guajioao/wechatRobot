import pymysql

# 连接mysql
conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='123456',charset='utf8',db='communitydb')
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

# 插入
def insert_user():
    insert_sql = "insert into server(wx_id,wx_name,authority) values(%(id)s,%(name)s,%(authority)s)"
    data = {
        "id": "wxid_y72ubiy0n2pq22",
        "name": "yy",
        "authority": "0"}
    cursor.execute(insert_sql, data)
    conn.commit()

# #查找
# def search_user(building,room):
#     print(f'查找房号为{room},楼号为{building}的用户\n')
#     search_user = "SELECT * FROM user WHERE room = %s AND building = %s";
#     params = (room,building)
#     cursor.execute(search_user,params)
#     userList = cursor.fetchall()
#     list_len = len(userList)
#     if list_len > 1:
#         print("找到的微信id大于1")
#     else:
#         wx_id = userList[0]['wx_id']
#         building = userList[0]['building']
#         room = userList[0]['room']
#         print(f"找到的微信id为{wx_id}")
    
#     print(userList[0])


#查找用户
#查找用户
def search_user_all(situation):
    search_all_user = "SELECT * FROM user "+situation;
    cursor.execute(search_all_user)
    userList = cursor.fetchall()
    return userList

def search_user(from_id,building,room):
    print(f'查找房号为{room},楼号为{building}的用户\n')
    search_to_user = "SELECT * FROM user WHERE room = %s AND building = %s";
    params1 = (room,building)
    cursor.execute(search_to_user,params1)
    userList = cursor.fetchall()
    list_len = len(userList)
    if list_len > 1 or list_len == 0:
        print(f"找到的微信id个数{list_len}")
        return None
    else:
        to_id = userList[0]['wx_id']
        print(f"找到的微信id为{to_id}")
        #寻找发送者
        building,room = search_user_byid(from_id)
        return to_id,building,room

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
    posList = []
    for user in userList:
        b = user['building']
        r = user['room']
        result = f"{b}-{r}"
        posList.append(result) #以8-401形式显示
    return posList

def send_located_list(wxid):
    list_pos = search_located_pos()
    msg = "当前已登记房间为:"+" ".join(list_pos)
    if wxid:
        print(msg)
        # wechat.send_text(to_wxid=wxid, content=msg)

def insert_message(msg_type,from_id,to_id,cont_type,content):
    print(f"从{from_id}向{to_id}发送类型为{msg_type}的内容:{content},内容类型为{cont_type}")
    insert_message = "insert into message(msg_type,from_id,to_id,cont_type,content) values(%s,%s,%s,%s,%s)"
    params = (msg_type,from_id,to_id,cont_type,content)
    cursor.execute(insert_message,params)
    conn.commit()
    print("插入message成功")

# send_located_list(1)
insert_message(1,1,2,1,"hi")
# search_user('wxid_zldk8ioij82c22',8,401)
# posList = search_located_pos()

#关闭连接
cursor.close()
conn.close()