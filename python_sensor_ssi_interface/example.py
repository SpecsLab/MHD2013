import sensor_reader as sr
import ssi_interface as si
import time
import signal
import sys


## SET FRAMES PER SECONDS HERE
fps = 100
time_delta = 1./fps

## SET PORT AND BAUDRATE HERE
port = "/dev/tty.usbmodem411"
baudrate = 115200


## BOARD ID 
board_id = "board1"
ssi_server_address = "0.0.0.0"


## INITIALIZE SENSOR(serialport,baud rate) and SSI INTERFACE(your board id, server address)
sensor = sr.SensorReader(port,baudrate)
ssi_send = si.SSI_interface_Sender(board_id, )
ssi_receive = si.SSI_interface_Receiver(board_id, ssi_server_address)
time.sleep(1)



def signal_handler(signal, frame):
	sensor.closeSensor()
	sys.exit(1)

	
time_start = time.time()

while True:

	signal.signal(signal.SIGINT, signal_handler)
	signal.signal(signal.SIGTSTP, signal_handler)
	signal.signal(signal.SIGQUIT, signal_handler)
	
	
	try:
			### read the sensor
			gsr = sensor.data[1]

			### send to ssi
			ssi_send.send_to_SSI([gsr],'send_gsr')

			### listen back from ssi
			arousal = ssi_receive.datapack["receive_gsr_arousal"]

			### limits the frame rate
			time_end = time.time()
			processing_time = time_end - time_start
			# print "processing_time  ", processing_time
			time_start = time_end
			time.sleep(max(0,time_delta-processing_time))

	
	except:
		pass






