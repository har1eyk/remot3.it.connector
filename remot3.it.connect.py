#!/Users/harley/anaconda3/bin/python

import json
from json import dumps
from urllib.request import urlopen
import requests
import httplib2
from terminaltables import AsciiTable
import subprocess
import pyperclip
import config

URL = config.URL
DEVELOPERKEY = config.DEVELOPERKEY
USERNAME = config.USERNAME
PASSWORD = config.PASSWORD

PAYLOAD = "{ \"username\" : \"%s\", \"password\" : \"%s\" }" % (USERNAME, PASSWORD)
HEADERS = {
    'developerkey': DEVELOPERKEY,
    'content-type': "application/json",
    'cache-control': "no-cache"
}
try:
    RESPONSE = requests.request("POST", URL, data=PAYLOAD, headers=HEADERS)
except ValueError:
    print("Error in making request to remot3.it")
    print(RESPONSE.status_code)

DATA = json.loads(RESPONSE.text)
# This is the token generated with every API call
token = (DATA['token'])


apiMethod = "https://"
apiServer = "api.remot3.it"
apiVersion = "/apv/v23.5"

# add the token here which you got from the /user/login API call
# token = "your login token"
deviceListURL = apiMethod + apiServer + apiVersion + "/device/list/all"
# print ("deviceListURL:", deviceListURL)
content_type_header = "application/json"
# print("Developer key is:", developerkey)
# print("token is:", token)
deviceListHeaders = {
    'Content-Type': content_type_header,
    'developerkey': DEVELOPERKEY,
    # you need to get token from a call to /user/login
    'token': token,
}

if __name__ == '__main__':
    httplib2.debuglevel = 0
    http = httplib2.Http()

    response, content = http.request(deviceListURL,
                                     'GET',
                                     headers=deviceListHeaders)
    myListOfDevicesJson = json.loads(content.decode('utf-8'))
    print("Token is:", token, "\t\t\tNumber of devices =",
          len(myListOfDevicesJson["devices"]) + 1)
    print("myListOfDevicesJson", myListOfDevicesJson["devices"])
    # for device in myListOfDevices["devices"]:
    # print (device["devicealias"])
    #print (myListOfDevicesJson["devices"][2])

    deviceListArray = [["No", "Active?", "Name", "LastContacted", "Created"]]
    i = 1
    # for d in (myListOfDevicesJson["devices"]):
    # 	if (d["devicestate"] == 'active'):
    # 		dArray = [ i, d["devicestate"], d["devicealias"], d["lastcontacted"], d["createdate"]]
    # 		deviceListArray.append(dArray)
    # 		i +=1
    for d in (myListOfDevicesJson["devices"]):
        dArray = [i, d["devicestate"], d["devicealias"],
                  d["lastcontacted"], d["createdate"]]
        deviceListArray.append(dArray)
        i += 1
    table = AsciiTable(deviceListArray)
    print(table.table)
inputString = input("Which sensor to connect? ")

# replace this with the actual UID of your device that you got from /device/list/all
chosenDeviceId = myListOfDevicesJson["devices"][int(
    inputString) - 1]["devicealias"]
UID = myListOfDevicesJson["devices"][int(inputString) - 1]["deviceaddress"]
print("you entered", inputString, "\tDevice ID:", chosenDeviceId, "UID:", UID)
print("other values", myListOfDevicesJson["devices"][int(inputString) - 1])

# you'll need to send a valid login token from /user/login

queried_ip = urlopen('http://ip.42.pl/raw').read().decode('utf-8'),
# ip address return in this format: b'192.59.106.43'
# need to truncate string on left due to addition of 1 "b" letter = bytes

home_ip = '216.15.40.152'
my_ip = str(queried_ip[0])
print("developerkey", DEVELOPERKEY)
print("token", token)
print("UID", UID)
print("IP address:", my_ip)

def proxyConnect(UID, token):
    httplib2.debuglevel = 0
    http = httplib2.Http()
    content_type_header = "application/json"

  # this is equivalent to "whatismyip.com"
  # in the event your router or firewall reports a malware alert
  # replace this expression with your external IP as given by
  # whatismyip.com

    proxyConnectURL = apiMethod + apiServer + apiVersion + "/device/connect"

    proxyHeaders = {
        'Content-Type': content_type_header,
        'developerkey': DEVELOPERKEY,
        'token': token
    }

    proxyBody = {
        'deviceaddress': UID,
        'hostip': my_ip,
        'wait': "true"
    }

    response, content = http.request(proxyConnectURL,
                                     'POST',
                                     headers=proxyHeaders,
                                     body=dumps(proxyBody),
                                     )
    try:
        print("Response", response)
        cnxnData = json.loads(content.decode('utf-8'))
        proxyLink = cnxnData["connection"]["proxy"]
        # ["connection"]["proxy"]
        # print ("Data is:\n", cnxnData)
        return proxyLink
    except KeyError:
        print("Key Error exception!")
        print("Content is:\n", content)


if __name__ == '__main__':
    proxyLink = proxyConnect(UID, token)
    # MYSTRING = "http://proxy8.yoics.net:32352"
    TRUNCSTRING = proxyLink[7:]
    PROXY = TRUNCSTRING[:-6]
    PORT = proxyLink[-5:]
    SSHPARAMS = 'ssh -l pi '+ PROXY +" -p "+ PORT

print("Connect to RPI:", SSHPARAMS)
print("Link is copied to the clipboard. CTRL-V")
pyperclip.copy(SSHPARAMS)
spam = pyperclip.paste()

 
# class ssh:
#     shell = None
#     client = None
#     transport = None
 
#     def __init__(self, address, username, password, sshport):
#         print("Connecting to server:", username, "@", str(address), "-p", sshport)
#         self.client = paramiko.client.SSHClient()
#         self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
#         self.client.connect(address, port=sshport, username=username, password=password, look_for_keys=False)

#         self.transport = paramiko.Transport((address, sshport))
#         self.transport.connect(username=username, password=password)
        
 
#         thread = threading.Thread(target=self.process)
#         thread.daemon = True
#         thread.start()
 
#     def closeConnection(self):
#         if(self.client != None):
#             self.client.close()
#             self.transport.close()
 
#     def openShell(self):
#         self.shell = self.client.invoke_shell()
 
#     def sendShell(self, command):
#         if(self.shell):
#             self.shell.send(command + "\n")
#         else:
#             print("Shell not opened.")
 
#     def process(self):
#         global connection
#         while True:
#             # Print data when available
#             if self.shell != None and self.shell.recv_ready():
#                 alldata = self.shell.recv(1024)
#                 while self.shell.recv_ready():
#                     alldata += self.shell.recv(1024)
#                 strdata = str(alldata, "utf8")
#                 strdata.replace('\r', '')
#                 print(strdata, end = "")
#                 if(strdata.endswith("$ ")):
#                     print("\n$ ", end = "")

# sshUsername = "pi"
# sshPassword = "agd1n"
# sshServer = PROXY
# sshPort = PORT
 
 
# connection = ssh(sshServer, sshUsername, sshPassword, int(PORT) )
# connection.openShell()
# while True:
#     command = input('$ ')
#     if command.startswith(" "):
#         command = command[1:]
#     connection.sendShell(command)
