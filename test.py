import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
data = 'name %s %s' % (5, '杜昌贵')
s.sendto(data.encode(), ('127.0.0.1', 9999))
s.close()