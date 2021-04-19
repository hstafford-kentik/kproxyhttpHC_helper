#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os
import sys
import threading
import time

try:
	hostName = sys.argv[1]
	hostPort = int(sys.argv[2])
except:
	print ("You need to enter a desired http healthcheck hostname and port.")
	print ("https is NOT supported.")
	print ("Example usage:  ./httpwrapper.py 0.0.0.0 8080")  
	exit()

httpCode = 404

# EDIT THE FOLLOWING IF YOU ARE RUNNING SOMETHING OTHER THAN THE DEFAULT VALUES!
kproxyIP = '127.0.0.1'  # yes, you could run this on a separate server from the kproxy itself
kproxyNetflowPort = 9995

def testKproxy(thisKproxyIP = '127.0.0.1', thisKproxyNetflowPort = 9995):
	# This function uses the built in healthcheck to look for "GOOD" in the output
	# this is done OUTSIDE of the webserver because sometimes it takes too long
	# and the http connection times out before a response header is created.

	result = os.popen('/bin/nc -w 5 '+thisKproxyIP+' '+str(thisKproxyNetflowPort+1)).read()
	if 'GOOD' in str(result):
		thishttpCode = 200
		#print('kproxy '+kproxyIP+' is up.')
	else:
		thishttpCode = 404
		#print('kproxy '+kproxyIP+' is down.')
	return (thishttpCode)

class MyServer(BaseHTTPRequestHandler):
	protocol_version = 'HTTP/1.1'
	def do_GET(self): 
		#if len(self.headers) == 1:  #Really janky and insecure way of only responding to ksynth agents
		if True: # meh, that makes it hard to troubleshoot, respond to anything.
			response = bytes('I sent you http response '+str(httpCode)+'.\n', 'utf-8')
			self.send_response(httpCode)
			self.send_header('Content-Type','text/plain; charset=utf-8')
			self.send_header("Content-Length", len(response))
			self.end_headers()
			#time.sleep(.25)
			#self.wfile.write(bytes('I sent http response '+str(httpCode)+'.\n', "utf-8"))
			self.wfile.write(response)
	def log_request(self, format, *args):
		return
		
# start the very simple webserver in a thread and pass it the up/down (200 or 404) kproxy status
myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))
thread = threading.Thread(target = myServer.serve_forever, args=(httpCode, ))
thread.daemon = True
thread.start()

try:
	while True:
		# Every 30 seconds, check the status of the kproxy.  This may be excessive, and could be 
		# done less frequently, since the synthetics agent can only check every minute anyway.
		httpCode = testKproxy(kproxyIP, kproxyNetflowPort)
		# print (httpCode)   ### just here for debugging.
		time.sleep(30)
except KeyboardInterrupt:
	pass
myServer.server_close()

print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))