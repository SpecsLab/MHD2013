import serial
import time
import signal
import sys
import threading as th


class SensorReader:

	def __init__(self, port, baudrate):

		self.data = [0.0,0.0,0.0]

		try:
			self.ser = serial.Serial(port, baudrate, timeout=1)
			print "serial connected"
			self.serial_read_thread = th.Thread(target=self.main)
			self.serial_read_thread.start()
			# return True
		except:
			print "cannot open serial : ("
			# return False

	def receiveSensor(self):
				
		try:


			self.line = self.ser.readline()
			try:
				self.data = [float(val) for val in self.line.split(';')]
				#print self.data

			except:

				pass

		except:

			print "serial reader missed one data point"


	def closeSensor(self):

		self.ser.close()
		sys.exit(0)
		print "serial disconnected"



	def main(self):

		time.sleep(1)
		
		while True:
			self.receiveSensor()











