import socket, cv2, pickle, struct
import pyshine as ps

mode = 'get'
name = 'CLIENT RECEIVING'

audio, context = ps.audioCapture(mode=mode)
ps.showPlot(context, name)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.32.167'
port = 4982

socket_address = (host_ip, port)
client_socket.connect(socket_address)
print("CLIENT CONNECTED TO", socket_address)

data = b""
audio_payload_size = struct.calcsize("Q")
video_payload_size = struct.calcsize("Q")

while True:
    # Audio
    while len(data) < audio_payload_size:
        packet = client_socket.recv(1024)  # Adjust this size as needed
        if not packet:
            break
        data += packet
    audio_packed_msg_size = data[:audio_payload_size]
    data = data[audio_payload_size:]
    audio_msg_size = struct.unpack("Q", audio_packed_msg_size)[0]

    while len(data) < audio_msg_size:
        packet = client_socket.recv(4*1024)  # Adjust this size as needed
        if not packet:
            break
        data += packet
    audio_frame_data = data[:audio_msg_size]
    data = data[audio_msg_size:]
    audio_frame = pickle.loads(audio_frame_data)
    audio.put(audio_frame)

    # Video
    while len(data) < video_payload_size:
        packet = client_socket.recv(4 * 1024)  # Adjust this size as needed
        if not packet:
            break
        
        data += packet
    video_packed_msg_size = data[:video_payload_size]
    data = data[video_payload_size:]
    video_msg_size = struct.unpack("Q", video_packed_msg_size)[0]

    while len(data) < video_msg_size:
        packet = client_socket.recv(4 * 1024)  # Adjust this size as needed
        if not packet:
            break
        data += packet
    video_frame_data = data[:video_msg_size]
    data = data[video_msg_size:]
    video_frame = pickle.loads(video_frame_data)
    # Process video frame as needed
    cv2.imshow("Received Video", video_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

client_socket.close()
cv2.destroyAllWindows()