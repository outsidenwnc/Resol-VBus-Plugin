#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################

################################################################################
# Imports
################################################################################
#import indigo
import urllib2
from xml.dom.minidom import parseString

################################################################################
# Globals
################################################################################
ipaddress = u"http://192.168.2.109:6432/"
#fields = {"currentCondition":'weather',"currentConditionIcon":'icon_url_name',"visibility":'visibility_mi',"temperatureF":'temp_f',"temperatureC":'temp_c',"temperatureString":'temperature_string',"humidity":'relative_humidity',"dewPointF":'dewpoint_f',"dewPointC":'dewpoint_c',"dewPointString":'dewpoint_string',"heatIndexF":'heat_index_f',"heatIndexC":'heat_index_c',"heatIndexString":'heat_index_string',"windDirection":'wind_dir',"windDegrees":'wind_degrees',"windMPH":'wind_mph',"windKnots":'wind_kt',"windString":'wind_string',"pressureInches":'pressure_in',"pressureMillibars":'pressure_mb',"location":'location',"latitude":'latitude',"longitude":'longitude'}

########################################

theUrl = ipaddress + u"description.xml"
print theUrl
try:
    f = urllib2.urlopen(theUrl)
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
print "Done"
