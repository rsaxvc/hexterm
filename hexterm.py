#!/usr/bin/python

#get all the arguments with argparse
import argparse
parser = argparse.ArgumentParser(description='Simple line-by-line hexadecimal serial terminal')
parser.add_argument("--port", help="Port name(example:COMA,COM1,/dev/ttyUSB0)")
parser.add_argument("--baud", help="Baud rate")
parser.add_argument("--parity", help="none,even,odd")
args = parser.parse_args()

if not args.port:
	args.port = "/dev/ttyUSB0"

if not args.baud:
	args.baud = "115200"
args.baud = int(args.baud)

import serial

if not args.parity or args.parity == "none":
	args.parity = serial.PARITY_NONE
elif args.parity == "even":
	args.parity = serial.PARITY_EVEN
elif args.parity == "odd":
	args.parity = serial.PARITY_ODD
else:
	print "unknown parity, assuming none"
	args.parity = serial.PARITY_NONE

ser = serial.Serial(args.port, args.baud, parity=args.parity, timeout=.1)

def bin2hex( bytes ):
	return ''.join('{:02x}'.format(byte) for byte in bytes)

def rxdaemon( ser ):
	while True:
		bytes = bytearray(ser.read(30))
		if len(bytes):
			print "RX:", bin2hex( bytes )

import thread
thread.start_new_thread ( rxdaemon, (ser,) )

import sys

while True:
	try:
		line = sys.stdin.readline()
	except KeyboardInterrupt:
		break

	if not line:
		break

	line=line.strip()
	if line=="":
		continue

	try:
		bytes = bytearray.fromhex(line)
	except ValueError:
		print "Not valid hex bytestring:",line
		continue

	print "TX:", bin2hex( bytes )
	ser.write(bytes)

ser.close()             # close port
