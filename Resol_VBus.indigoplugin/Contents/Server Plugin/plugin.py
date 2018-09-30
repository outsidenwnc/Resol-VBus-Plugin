#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################

################################################################################
# Imports
################################################################################
#import indigo
import urllib2
from xml.dom.minidom import parseString
import socket

################################################################################
# Globals
################################################################################
ipaddress = u"http://192.168.2.109"
#fields = {"currentCondition":'weather',"currentConditionIcon":'icon_url_name',"visibility":'visibility_mi',"temperatureF":'temp_f',"temperatureC":'temp_c',"temperatureString":'temperature_string',"humidity":'relative_humidity',"dewPointF":'dewpoint_f',"dewPointC":'dewpoint_c',"dewPointString":'dewpoint_string',"heatIndexF":'heat_index_f',"heatIndexC":'heat_index_c',"heatIndexString":'heat_index_string',"windDirection":'wind_dir',"windDegrees":'wind_degrees',"windMPH":'wind_mph',"windKnots":'wind_kt',"windString":'wind_string',"pressureInches":'pressure_in',"pressureMillibars":'pressure_mb',"location":'location',"latitude":'latitude',"longitude":'longitude'}

########################################
theUrl1 = ipaddress + u":6432/description.xml"
print theUrl1
try:
    f = urllib2.urlopen(theUrl1)
except urllib2.HTTPError, e:
    print("HTTP error getting station data")
except Exception, e:
    print("Unknown error getting station data")
theXml = f.read()
theDocTree = parseString(theXml)
# parse out the elements - check observation date first and only continue if it's changed
try:
    y = theDocTree.getElementsByTagName('friendlyName')[0].firstChild.data
    print "friendlyName = ", y
except IndexError:
    print("Index error ")
##
theUrl2 = ipaddress + u"/cgi-bin/get_resol_device_information"
#
try:
    response = urllib2.urlopen(theUrl2)
except urllib2.HTTPError, e:
    print("HTTP error getting station data")
except Exception, e:
    print("Unknown error getting station data")
#
print (response.read())
#
TCP_IP = '192.168.2.109'
TCP_PORT = 7053
BUFFER_SIZE = 2048
pw = "PASS vbus"
vbuscmd = "DATA"
recvd_data = 0
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
data = s.recv(BUFFER_SIZE)
str_len=len(data)
recvd_data += str_len
print "recieved data", recvd_data
print "received data:", data, str_len
if data.strip() == '+HELLO':
    s.send(pw)
    print "true"
else:
    print "false"
    print data
data2 = s.recv(BUFFER_SIZE)
print data2
if data2.count("+OK") > 0:
    print  data2.count("+OK")
    print len(data2)
    recvd_data += len(data2)
    s.send(vbuscmd)
data4=s.recv(BUFFER_SIZE)
recvd_data += len(data4)
print data4
if data4.count("+OK") > 0:
    print  data4
    while 79  > len(data2):
        print "in while loop"
        #s.send()
        data3 = s.recv(BUFFER_SIZE)
        recvd_data += len(data3)
        print "data3", data3, "recvd data", recvd_data
else:
    print "data command not accepted"
s.close()
print "Done"
