import socketio

sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins="*"
)

sio_app = socketio.ASGIApp(
    socketio_server=sio,
    socketio_path='sockets'
)



# Estrutura para armazenar os usuários por sala
# Exemplo: {'sala1': ['user1', 'user2'], 'sala2': ['user3']}
rooms_users = {}

@sio.event
async def connect(sid, environ):
    print(f"Usuário {sid} conectado")

@sio.event
async def disconnect(sid):
    for room in rooms_users:
        if sid in rooms_users[room]:
            rooms_users[room].remove(sid)
            await sio.emit('message', {'response': f'Usuário {sid} saiu da sala {room}'}, room=room)
            sio.leave_room(sid, room)
            # Se a sala estiver vazia, remova-a da estrutura
            if not rooms_users[room]:
                del rooms_users[room]

@sio.event
async def join_room(sid, data):
    room_name = data["room"]
    sio.enter_room(sid, room_name)
    print(f"Usuário {sid} entrou na sala {room_name}")
    # Adicione o usuário à sala na estrutura
    if room_name not in rooms_users:
        rooms_users[room_name] = []
    rooms_users[room_name].append(sid)

    await sio.emit('message', {'response': f'Usuário {sid} entrou na sala {room_name}'}, room=room_name)

@sio.event
async def message(sid, message):
    print(f"Usuário {sid} enviou a mensagem {message['message']} para a sala {message['room']}")
    await sio.emit("message", {"message": message["message"]}, room=message["room"])

@sio.event
async def leave_room(sid, data):
    room_name = data["room"]
    sio.leave_room(sid, room_name)

    # Remova o usuário da sala na estrutura
    if room_name in rooms_users:
        rooms_users[room_name].remove(sid)
        # Se a sala estiver vazia, remova-a da estrutura
        if not rooms_users[room_name]:
            del rooms_users[room_name]

    await sio.emit('message', {'response': f'Usuário {sid} saiu da sala {room_name}'}, room=room_name)

@sio.event
async def get_users_in_room(sid, room_name):
    users_in_room = rooms_users.get(room_name, [])
    await sio.emit("users_in_room_response", {'users':users_in_room}, room=sid)


