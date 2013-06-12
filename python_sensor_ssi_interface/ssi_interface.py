import socket
import struct
import json
from OSC import OSCServer, OSCClient, OSCMessage
import threading as th



class SSI_interface_Sender:

	def __init__(self, board_id, address):

		try:
			self.ports_config = json.loads(open("ssi_ports.json").read())
			print "ports config loaded"
		except:
			print "couldn't load ports file"
		self.client_socket_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.board_id = board_id
		self.address = address

	def send_to_SSI(self, data, measure_name):

		port = self.ports_config[self.board_id][measure_name]


		for d in data:
			pack = struct.pack('<f',d)
			self.client_socket_send.sendto(pack, (self.address, port))


class SSI_interface_Receiver:

	def __init__(self, board_id, measure):

		try:
			self.ports_config = json.loads(open("ssi_ports.json").read())
			print "ports config loaded"
		except:
			print "couldn't load ports file"
		self.measure = measure
		self.port= self.ports_config[board_id][self.measure]
		self.myOSC_Server = OSCServer( ("" , self.port ))
		
		self.myOSC_Server.addMsgHandler("/strm", self.receiveStream)
		self.myOSC_Server.addMsgHandler("/evnt", self.receiveEvent)
		self.myOSC_Server.addMsgHandler("/text", self.receiveText)

		self.datapack = {

				"receive_ecg":0,
				"receive_ecg-hr":0,
				"receive_ecg-rspike":0,
				"receive_ecg-pulse":0,
				"receive_ecg-tdf":0,
				"receive_ecg-sdf":0,

				"receive_gsr":0,
				"receive_gsr_pre":0,
				"receive_gsr_arousal":0,
				"receive_gsr_peak":0,
				"receive_gsr_slope":0,
				"receive_gsr_drop":0,

				"air":0,
				"air_pre":0,
				"air_pulse":0,
				"air_exhale":0

			}

		self.osc_thread = th.Thread(target=self.main)
		self.osc_thread.start()

		
	def receiveStream(self, addr, tags, data, source):

		data[7] = self.readBlob(data[7])
		self.datapack[self.measure] = data

	def receiveEvent(self, addr, tags, data, source):

		data[7] = self.readBlob(data[7])
		self.datapack[self.measure] = data

	def receiveText(self, addr, tags, data, source):

		data[7] = self.readBlob(data[7])
		self.datapack[self.measure] = data

	def readBlob(self, binary):
		decoded = []
		for i in range(len(binary)):
			if i%4 == 0 and i != 0:
				decoded.append(struct.unpack('f', binary[i-4:i])[0])
		
		return decoded


	def main(self):
		print "osc is listening"
		self.myOSC_Server.serve_forever()



