from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.secret_key = 'random secret key!'
# 允许所有来源的跨域请求，生产环境中可根据需要调整
socketio = SocketIO(app, cors_allowed_origins="*")

# 处理用户加入房间的事件
@socketio.on('join')
def join(message):
    username = message['username']
    room = message['room']
    join_room(room)
    print(f'RoomEvent: {username} has joined the room {room}\n')
    emit('ready', {'username': username}, to=room, skip_sid=request.sid)

# 处理用户发送数据的事件
@socketio.on('data')
def transfer_data(message):
    username = message['username']
    room = message['room']
    data = message['data']
    print(f'DataEvent: {username} has sent the data:\n {data}\n')
    # 发送数据时需要携带username信息
    emit('data', {'username': username, 'data': data}, to=room, skip_sid=request.sid)

# 处理默认错误
@socketio.on_error_default
def default_error_handler(e):
    """_summary_

    Args:
        e (_type_): _description_
    """
    print(f"Error: {e}")
    socketio.stop()

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=9000)
