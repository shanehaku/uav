# coding=utf-8
import threading
import cv2
import time
import socket

host = ""
port = 9000
locaddr = (host, port)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(locaddr)


def recv():
    while True:
        try:
            # 監聽此socket，當收到資料的時候就會執行 data, server = sock.recvfrom(1518)
            # data為本機收到的資料，資料須先用utf-8解碼後才會變成字串
            # server為無人機的IP
            data, server = sock.recvfrom(1518)
            print("{} : {}".format(server, data.decode(encoding="utf-8")))
        except Exception:
            print("\nExit . . .\n")
            break


recvThread = threading.Thread(target=recv)
recvThread.start()
print("start recv")

messages = [
    "command",
    "battery?",
    "streamon",
]

uavIp = "192.168.10.1"

print("start commands")
for i in range(0, len(messages)):
    msg1 = messages[i]
    sock.sendto(msg1.encode("utf-8"), (uavIp, 8889))
    time.sleep(5)

cap = cv2.VideoCapture("udp://" + uavIp + ":11111")

print("start capture")
while True:
    isFrame, frame = cap.read()
    print(isFrame)
    if isFrame:
        cv2.imshow("UAV video", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
