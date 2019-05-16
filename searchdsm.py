#!/usr/bin/env python3
#!-*- coding:utf-8 -*-
import socket
import re
import binascii
#import uuid
import sys


_author_ = 'wrysunny'
_info_ = 'synology assistant for python'


print(f'python3 {sys.argv[0]} <IP> <MAC> <== 54:ee:75:d2:f0:dd')
srcip =   sys.argv[1] 
srcport = 1234
desip = '<broadcast>'
desport = 9999
mac = sys.argv[2]

#def getmac():
#	mac = uuid.UUID(int = node).hex[-12:]
#	mac = ':'.join(mac[i:i+2] for i in range(0, len(mac), 2))
mac = str(binascii.b2a_hex(mac.encode()))[2:]
payload = f'1234567853594e4fa40400000201a60478000000010401000000b008c001000000000000b1080000000000000000b808c001000000000000b90800000000000000007c11{mac}7c11{mac}7c11{mac}7c11{mac}'.replace("'",'')
payload = binascii.a2b_hex(payload)
print(payload)

def send_payload():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	s.bind((srcip,srcport))
	for i in range(5):
		s.sendto(payload, (desip,desport))
	s.close()

def recvfrom():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	s.bind((srcip, desport))
	while True:
		(buf,address) = s.recvfrom(4096)
		if not len(buf):
			break
		address = str(address)[2:-8]
		if address != srcip:
			strs = str(buf)
			mac = re.findall(r"\\x124VxSYNO\\x19\\x11(.+?)\\x12\\x04\\xc0\\xa8W",strs)
			name = re.findall(r"\\x04\\x02\\x00\\x00\\x00\\x11(.+?)\\x1e\\x04\\xc0",strs)
			sn = re.findall(r"\\x04\\x0c\\x00\\x00\\x00\\xc0(.+?)\\xa4\\x04\\x00\\x00\\x02\\x01",strs)
			ver = re.findall(r"\\x10]\\x00\\x00w\\x05(.+?)\\x90\\x04",strs)
			model = re.findall(r"\\x00\\x00\\x00x(.+?)\\xc1\\x03DSM\\x80",strs)
			macadr = str(mac)[2:-2]
			pname = str(name)[7:-2]
			serinal =str(sn)[5:-16]
			ver = str(ver)[2:-2]
			model = str(model)[7:-2]
			info = f'IP:{address} NAME:{pname} MAC:{macadr} SN:{serinal} version:{ver} Model:{model}\t\n'
			with open('log.txt','a+') as f:
				f.write(info)
			print(info)


if __name__ == '__main__':
	send_payload()
	recvfrom()