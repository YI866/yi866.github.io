from __future__ import absolute_import
from gevent import monkey
monkey.patch_all()
import socketio
from flask import Flask, request, jsonify, Response
from flask_socketio import SocketIO, emit, join_room,\
    leave_room, disconnect, send, rooms


app = Flask(__name__)
mgr = socketio.RedisManager('redis://localhost:6379/2')
socket_io = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="gevent",
    client_manager=mgr,
    logger=True,
    engineio_logger=True,
)


@socket_io.on('connect', namespace='/ikas')
def on_connect(data):
    print('%s connected success' % request.sid)

@socket_io.on('disconnect', namespace='/ikas')
def on_disconnect():
    print('%s disconnected' % request.sid)

@socket_io.on('join_room', namespace='/ikas')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room, request.sid)
    print(username + ' has entered the room.')
    socket_io.send('you has entered the room.', namespace='/ikas')
    socket_io.send(username + ' has entered the room.', to=room, broadcast=True, namespace='/ikas')

@socket_io.on('leave', namespace='/ikas')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room, request.sid)
    print(username + ' has left the room.')
    socket_io.send('you has left the room.', namespace='/ikas')
    socket_io.send(username + ' has left the room.', to=room, broadcast=True, namespace='/ikas')

@socket_io.on('rooms list', namespace='/ikas')
def rooms_list(data):
    print(rooms(request.sid))

@socket_io.on('exit', namespace='/ikas')
def exit(data):
    disconnect(request.sid)
    print(rooms(request.sid))

@app.route('/drive', methods=['POST'])
def drive():
    data = request.json
    sid = data.get('sid')
    username = data.get('username')
    room = data.get('room')
    msg = data.get('msg')
    # socket_io.emit('receipt', msg, to=room, broadcast=True, namespace='/ikas')
    socket_io.emit('receipt', msg, to=room, namespace='/ikas')
    socket_io.send(msg, to=room, broadcast=True, namespace='/ikas')
    # disconnect(sid, namespace='/ikas')
    return Response('OVER', status=200)

socket_io.run(app=app, host='0.0.0.0', port=8080)