import socket, cv2, numpy as np
import uuid

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  
s.bind(('192.168.8.103', 3334))
s.listen(5)
  
while 1:
    conn, addr = s.accept()

    import os
    try:
        os.mkdir(addr[0])
    except:
        pass

    f = open(addr[0] + '/' + str(len(os.listdir(addr[0]))) + '.jpg', 'wb')
  
    while 1:
        recv = conn.recv(1024)
        
        f.write(recv)
  
        if not recv:
            break
    
    f.close()