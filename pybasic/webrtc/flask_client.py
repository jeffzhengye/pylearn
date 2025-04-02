import socketio

# 创建SocketIO客户端实例
sio = socketio.Client()

# 连接成功的回调函数
@sio.event
def connect():
    print('Connected to server')
    # 模拟用户加入房间
    username = "user1"
    room = "room1"
    sio.emit('join', {'username': username, 'room': room})

# 接收到'ready'事件的回调函数
@sio.on('ready')
def on_ready(data):
    print(f"Received ready event: {data}")

# 接收到'data'事件的回调函数
@sio.on('data')
def on_data(data):
    print(f"Received data: {data}")

# 模拟发送数据的函数
def send_message():
    message = "Hello, this is a test message!"
    username = "user1"
    room = "room1"
    return sio.emit('data', {'username': username, 'room': room, 'data': message})

if __name__ == '__main__':
    try:
        print(f"start")
        sio.connect('http://127.0.0.1:9000')
        send_message()
        sio.wait()
    except socketio.exceptions.ConnectionError:
        print("Could not connect to the server")
