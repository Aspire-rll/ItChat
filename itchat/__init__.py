import time

from .client import client
from . import content # this is for creating pyc

__version__ = '1.1.6'

__client = client()
def auto_login(hotReload=False, statusStorageDir='itchat.pkl', enableCmdQR=False):
    if hotReload:
        if __client.load_login_status(statusStorageDir): return
        __client.auto_login(enableCmdQR=enableCmdQR)
        __client.dump_login_status(statusStorageDir)
    else:
        __client.auto_login(enableCmdQR=enableCmdQR)

# The following method are all included in __client.auto_login >>>
def get_QRuuid(): return __client.get_QRuuid()
def get_QR(uuid=None, enableCmdQR=False): return __client.get_QR(uuid, enableCmdQR)
def check_login(uuid=None): return __client.check_login(uuid)
def web_init(): return __client.web_init()
def get_friends(update=False): return __client.get_friends(update)
def show_mobile_login(): return __client.show_mobile_login()
def start_receiving(): return __client.start_receiving()
# <<<

# The following methods are for reload without re-scan the QRCode >>>
def dump_login_status(fileDir='itchat.pkl'): return __client.dump_login_status(fileDir)
def load_login_status(fileDir='itchat.pkl'): return __client.load_login_status(fileDir)
# <<<

# The following methods are for contract dealing >>>
def search_friends(name=None, userName=None, remarkName=None, nickName=None, wechatAccount=None):
    return __client.storageClass.search_friends(name, userName, remarkName, nickName, wechatAccount)
def set_alias(userName, alias): return __client.set_alias(userName, alias)
def add_friend(userName, status=2, ticket='', userInfo={}): return __client.add_friend(status, userName, ticket, userInfo)
def get_mps(update=False): return __client.get_mps(update)
def search_mps(name=None, userName=None): return __client.storageClass.search_mps(name, userName)
def get_chatrooms(update=False): return __client.get_chatrooms(update)
def search_chatrooms(name=None, userName=None): return __client.storageClass.search_chatrooms(name, userName)
def update_chatroom(groupUserName): return __client.update_chatroom(groupUserName)
def create_chatroom(memberList, topic = ''): return __client.create_chatroom(memberList, topic)
def delete_member_from_chatroom(chatRoomUserName, memberList): return __client.delete_member_from_chatroom(chatRoomUserName, memberList)
def add_member_into_chatroom(chatRoomUserName, memberList): return __client.add_member_into_chatroom(chatRoomUserName, memberList)
# <<<

# The following is the tear of age, will be deleted soon
def get_batch_contract(groupUserName): return __client.update_chatroom(groupUserName)
# <<<

# if toUserName is set to None, msg will be sent to yourself
def send_msg(msg = 'Test Message', toUserName = None): return __client.send_msg(msg, toUserName)
def send_file(fileDir, toUserName): return __client.send_file(fileDir, toUserName)
def send_video(fileDir, toUserName): return __client.send_video(fileDir, toUserName)
def send_image(fileDir, toUserName): return __client.send_image(fileDir, toUserName)
def send(msg, toUserName = None):
    if msg is None: return False
    if msg[:5] == '@fil@':
        return __client.send_file(msg[5:], toUserName)
    elif msg[:5] == '@img@':
        return __client.send_image(msg[5:], toUserName)
    elif msg[:5] == '@msg@':
        return __client.send_msg(msg[5:], toUserName)
    elif msg[:5] == '@vid@':
        return __client.send_video(msg[5:], toUserName)
    else:
        return __client.send_msg(msg, toUserName)

# decorations
__functionDict = {'GroupChat': {}, 'GeneralReply': None}
def configured_reply():
    if not __client.storageClass.msgList: return
    msg = __client.storageClass.msgList.pop()
    if '@@' in msg.get('FromUserName'):
        replyFn = __functionDict['GroupChat'].get(msg['Type'], __functionDict['GeneralReply'])
        if replyFn: send(replyFn(msg), msg.get('FromUserName'))
    else:
        replyFn = __functionDict.get(msg['Type'], __functionDict['GeneralReply'])
        if replyFn: send(replyFn(msg), msg.get('FromUserName'))

def msg_register(_type=None, *args, **kwargs):
    if hasattr(_type, '__call__'):
        __functionDict['GeneralReply'] = _type
        return configured_reply
    elif _type is None:
        return configured_reply
    else:
        if not isinstance(_type, list): _type = [_type]
        def _msg_register(fn, *_args, **_kwargs):
            for msgType in _type:
                if kwargs.get('isGroupChat', False):
                    __functionDict['GroupChat'][msgType] = fn
                else:
                    __functionDict[msgType] = fn
        return _msg_register

# in-build run
def run():
    print('Start auto replying')
    try:
        while 1:
            configured_reply()
            time.sleep(.3)
    except KeyboardInterrupt:
        print('Bye~')
