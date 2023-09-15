const socket = io.connect('http://localhost:8000', {
        path: '/sockets'
    });
// Quando receber uma nova mensagem do servidor
socket.on('message', function(data) {
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('div');
    messageElement.innerText = data.message;
    chatBox.appendChild(messageElement);
});
socket.on('users_in_room_response',function(data){
    console.log(data);
})

socket.on('connect',() =>{
    socket.emit('join_room',{room:'sala1'});
    socket.emit('get_users_in_room','sala1');
})
const sendButton = document.getElementById('send-button');
sendButton.addEventListener('click', function() {
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value;
    if (message) {
        socket.emit('message', { message: message,room:'sala1' }); // Enviar mensagem para o servidor
        messageInput.value = ''; // Limpar input
    }
});
