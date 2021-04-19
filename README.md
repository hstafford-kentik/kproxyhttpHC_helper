# kproxyhttpHC_helper

This is a simple server that allows one to check the status of Kentik kproxy via http instead of the 
built in telnet/nc port.

1) Edit the HChttpwrapper.py script to reflect the netflow port in use, as well as the IP (if needed)
2) Copy HChttpwrapper.py to /usr/bin/HChttpwrapper.py and make sure it's executable: "chmod +x /usr/bin/HChttpwrapper.py"
3) Copy the .service file to /etc/systemd/system/ and edit as needed to use whatever IP/port you'd like to use
   for your http check.
4) Run "systemctl start HChttpwrapper.service" to start it, then "systemctl status HChttpwrapper.service" to check it.
5) If that worked, run ""systemctl enable HChttpwrapper.service" so that it will run at reboot.
6) Maybe "wget 127.0.0.1 80" to check that it's responding?
7) Set up Kentik synthetics http test to check this service and notify if an http Status Code 200 is not recieved.

This is NOT a supported service/application.  Do not contact Kentik support regarding issues with this service - it is
offered only as a courtesy to users who wish to incorporate synthetic agent monitoring of kproxy servers.