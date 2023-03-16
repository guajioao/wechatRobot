import re


def func1():
    pattern = r'-|\s'
    test_string = 'foo-bar-hello-world-123-456'

    result_list = list(
        filter(lambda x: x != '', re.split(pattern, test_string)))
    print(result_list)
def func2():
    # 定义匹配模式
    pattern = r'(.+?)小区-(\w+)栋-(.+)'

    # 定义测试字符串
    test_string = 'xx小区-x栋-xx'

    # 进行匹配
    match_obj = re.match(pattern, test_string)

    # 将匹配到的信息保存为字典形式
    result_dict = {'community': match_obj.group(1), 'building': match_obj.group(2), 'room': match_obj.group(3)}

    # 输出结果
    print(result_dict)
def func3():
    address_pattern = r'(.+?)-(\d+)栋-(\d+)?号'
    address_string = 'xx小区-1栋-101'

    match = re.match(address_pattern, address_string)
    if match:
        address_dict = {
            'community': match.group(1),
            'building': match.group(2),
            'room': match.group(3)
        }
        print(address_dict)
    else:
        print('不符合要求的地址格式')

# func1
# func3()
# 定义匹配模式
def fun4c():

    pattern = r'(.+?)小区-?(\w*?)(?:栋)?-(.+)'
    #通过使用(?:栋)?的非捕获分组来允许栋字可以不出现
    r'(.+?)小区-?(\w*?)(?:栋)?-(.+)'
    # 定义测试字符串
    test_string1 = 'xx小区-x栋-xx'
    test_string2 = 'xx小区-x-xx'

    # 进行匹配
    match_obj1 = re.match(pattern, test_string1)
    match_obj2 = re.match(pattern, test_string2)

    # 将匹配到的信息保存为字典形式
    result_dict1 = {'community': match_obj1.group(1), 'building': match_obj1.group(2) or '', 'room': match_obj1.group(3)}
    result_dict2 = {'community': match_obj2.group(1), 'building': match_obj2.group(2) or '', 'room': match_obj2.group(3)}

    # 输出结果
    print(result_dict1)  # {'community': 'xx', 'building': 'x', 'room': 'xx'}
    print(result_dict2)  # {'community': 'xx', 'building': 'x', 'room': 'xx'}

def func5():
    # 定义测试字符串
    msg = "to:8-401 hi"
    split_list = msg.split(' ', 1)  # 以空格为分隔符，分割成两个部分
    to_part = split_list[0].split(':')[1]  # 获取冒号后面的部分
    content_part = split_list[1]  # 获取空格后面的部分
    result_dict = {'to': to_part, 'content': content_part}  # 存储为字典
    print(result_dict)


    
def handle_contact_msg(data):
    msg = data
    print("msg:",msg)
    split_list = msg.split(' ', 1)  # 以空格为分隔符，分割成两个部分
    if len(split_list)<=1: 
        split_list = msg.split('\n', 1)  # 以空格为分隔符，分割成两个部分
    # to_position = split_list[0].split(':')[1]  # 获取房间号8-401
    to_position = split_list[0]  # 获取房间号8-401
    content = split_list[1]  # 获取空格后面的部分
    pattern = r'\d-\d'

    #判断content是否符合验证信息格式
    if re.match( pattern, to_position) is not None:
        print("匹配成功,格式正确")
        data = re.findall("(.*)-(.*)", to_position)[0]  # data为元组格式('8','401')
        building = data[0]  # 获取楼号'8'
        room = data[-1]  # 获取房号'401'
        # to_wxid = search_user_byPos(building,room)
    else:
        to_wxid = None
      # 获取冒号后面的部分
    result_dict = {'to_id': to_wxid, 'content': content,'building': building,'room':room}  # 存储为字典
    return result_dict



#分类收到的类型
def judge_msg(data):
    #1:匿名信息;2.不匿名信息；3.其他信息
    is_send = judge_send(data)
    if type(is_send) == tuple:
        if is_send[0]:#如果为通讯
            contact_type = is_send[1]
            content = is_send[2]
            return contact_type,content
    else:#关键词查找
        type_word = judge_word(data)
        return type_word


def judge_send(data):
    msg = data
    split_list = msg.split('to:', 1)  # 以空格为分隔符，分割成两个部分
    type_send = split_list[0]
    result = True
    if len(split_list) <= 1:#以防：为中文字符
        split_list = msg.split('to：', 1)
        type_send = split_list[0]
    if len(split_list) <= 1:#以防未输入：
        split_list = msg.split('to', 1)
        type_send = split_list[0]
    if len(split_list) <= 1:#不是发消息
        return False
    if type_send == "匿名":
        print(f"1:type = {type_send},list = {split_list[1]}")
        USER_CONTACT = 1
        return result,USER_CONTACT,split_list[1]
    elif type_send == "不匿名":
        print(f"2:type = {type_send},list = {split_list[1]}")
        USER_CONTACT = 2
        return result,USER_CONTACT,split_list[1]
    else:#默认匿名
        print(f"3:type = {type_send},list = {split_list[0]}")
        USER_CONTACT = 1
        return result,USER_CONTACT,split_list[0]

def judge_word(data):
    HELP_MSG = 3
    ERROR_MSG = -1
    if data == "帮助":
        return HELP_MSG
    else:
        return ERROR_MSG

# func5()

type,content_list = judge_msg("帮助")
# type,content_list = judge_msg("不匿名to8-402 好嗷")
handle_contact_msg(content_list)