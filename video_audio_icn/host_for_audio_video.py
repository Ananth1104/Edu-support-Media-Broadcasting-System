import socket, cv2, pickle, struct
import pyshine as ps

mode = 'send'
name = 'SERVER TRANSMITTING'

audio, context = ps.audioCapture(mode=mode)
cap = cv2.VideoCapture(0)  # assuming you want to capture video from the default camera

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.32.254'
port = 4982
backlog = 5
socket_address = (host_ip, port)
print('STARTING SERVER AT', socket_address, '...')
server_socket.bind(socket_address)    
server_socket.listen(backlog)

while True:
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    if client_socket:
        while True:
            # Audio
            audio_frame = audio.get()
            audio_data = pickle.dumps(audio_frame)
            audio_message = struct.pack("Q", len(audio_data)) + audio_data
            client_socket.sendall(audio_message)

            # Video
            ret, video_frame = cap.read()
            video_data = pickle.dumps(video_frame)
            video_message = struct.pack("Q", len(video_data)) + video_data
            client_socket.sendall(video_message)



client_socket.close()