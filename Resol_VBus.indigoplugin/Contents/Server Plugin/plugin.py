#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2016, Perceptive Automation, LLC. All rights reserved.
# http://www.indigodomo.com
#

################################################################################
# Imports
################################################################################
import indigo
import urllib2
from xml.dom.minidom import parseString

################################################################################
# Globals
################################################################################
theUrlBase = u"http://www.weather.gov/xml/current_obs/"
fields = {"currentCondition":'weather',"currentConditionIcon":'icon_url_name',"visibility":'visibility_mi',"temperatureF":'temp_f',"temperatureC":'temp_c',"temperatureString":'temperature_string',"humidity":'relative_humidity',"dewPointF":'dewpoint_f',"dewPointC":'dewpoint_c',"dewPointString":'dewpoint_string',"heatIndexF":'heat_index_f',"heatIndexC":'heat_index_c',"heatIndexString":'heat_index_string',"windDirection":'wind_dir',"windDegrees":'wind_degrees',"windMPH":'wind_mph',"windKnots":'wind_kt',"windString":'wind_string',"pressureInches":'pressure_in',"pressureMillibars":'pressure_mb',"location":'location',"latitude":'latitude',"longitude":'longitude'}

########################################
#create function to update indigo variables or create if it does not exist
def updateVar(name, value, folder=0):
	if name not in indigo.variables:
		indigo.variable.create(name, value=value, folder=folder)
	else:
		indigo.variable.updateValue(name, value)

################################################################################
class Plugin(indigo.PluginBase):
	########################################
	# Class properties
	########################################

	########################################
	def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
		super(Plugin, self).__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
		self.debug = pluginPrefs.get("showDebugInfo", False)
		self.deviceList = []

	########################################
	def goToStationURL(self, valuesDict, typeId, devId):
		self.browserOpen("http://www.weather.gov/xml/current_obs/")

	########################################
	def deviceStartComm(self, device):
		self.debugLog("Starting device: " + device.name)
		if device.id not in self.deviceList:
			self.update(device)
			self.deviceList.append(device.id)
			device.updateStateImageOnServer(indigo.kStateImageSel.TemperatureSensor)

	########################################
	def deviceStopComm(self, device):
		self.debugLog("Stopping device: " + device.name)
		if device.id in self.deviceList:
			self.deviceList.remove(device.id)

	########################################
	def runConcurrentThread(self):
		self.debugLog("Starting concurrent tread")
		try:
			while True:
				# we sleep (30 minutes) first because when the plugin starts, each device
				# is updated as they are started.
				self.sleep(30 * 60)
				# now we cycle through each station
				for deviceId in self.deviceList:
					# call the update method with the device instance
					self.update(indigo.devices[deviceId])
		except self.StopThread:
			pass

	########################################
	def update(self,device):
		self.debugLog("Updating device: " + device.name)
		# download the file
		theUrl = theUrlBase + device.pluginProps["address"] + u".xml"
		try:
			f = urllib2.urlopen(theUrl)
		except urllib2.HTTPError, e:
			self.errorLog("HTTP error getting station %s data: %s" % (device.pluginProps["address"], str(e)))
			return
		except Exception, e:
			self.errorLog("Unknown error getting station %s data: %s" % (device.pluginProps["address"], str(e)))
			return
		theXml = f.read()
		theDocTree = parseString(theXml)
		# parse out the elements - check observation date first and only continue if it's changed
		try:
			observationDate = theDocTree.getElementsByTagName('observation_time_rfc822')[0].childNodes[0].data
		except IndexError:
			self.errorLog("File didn't contain an observation date for station %s - possible corrupt data file from NOAA" % (device.pluginProps["address"],))
			return
		if (observationDate != device.states["observationDate"]):
			keyValueList = []
			keyValueList.append({'key':'observationDate', 'value':observationDate})
			for state,fieldName in fields.iteritems():
				try:
					newValue = theDocTree.getElementsByTagName(fieldName)[0].childNodes[0].data
				except IndexError:
					newValue = "- data unavailable -"
				self.updateKeyValueList(device, state, newValue, keyValueList)
			device.updateStatesOnServer(keyValueList)

	########################################
	def updateKeyValueList(self, device, state, newValue, keyValueList):
		if (newValue != device.states[state]):
			if state == "currentConditionIcon":
				newValue = newValue.split(".")[0]
			keyValueList.append({'key':state, 'value':newValue})

	########################################
	# UI Validate, Close, and Actions defined in Actions.xml:
	########################################
	def validateDeviceConfigUi(self, valuesDict, typeId, devId):
		stationId = valuesDict['address'].encode('ascii','ignore').upper()
		valuesDict['address'] = stationId
		theUrl = theUrlBase + stationId + ".xml"
		try:
			urllib2.urlopen(theUrl)
		except urllib2.HTTPError, e:
			errorsDict = indigo.Dict()
			errorsDict['address'] = "Station not found or isn't responding"
			self.errorLog("Error getting station %s data: %s" % (stationId, str(e)))
			return (False, valuesDict, errorsDict)
		return (True, valuesDict)

	########################################
	# Menu Methods
	########################################
	def toggleDebugging(self):
		if self.debug:
			indigo.server.log("Turning off debug logging")
			self.pluginPrefs["showDebugInfo"] = False
		else:
			indigo.server.log("Turning on debug logging")
			self.pluginPrefs["showDebugInfo"] = True
		self.debug = not self.debug

