# -*- coding: UTF-8 -*-
#######################################################################
#
#    PiconsTestConverter
#    Copyright (C) 2013 by svox
#
#    In case of reuse of this source code please do not remove this copyright.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    For more information on the GNU General Public License see:
#    <http://www.gnu.org/licenses/>.
#
#######################################################################

import os, re, shutil, unicodedata

from enigma import eServiceCenter, eServiceReference
from Components.ActionMap import ActionMap
from Screens.Screen import Screen
from Components.ConfigList import ConfigListScreen
from ServiceReference import ServiceReference

#######################################################################


class PiconsTestConverterView(Screen):
    skin = """
          <screen name="PiconsTestConverter-Setup" position="0,0" size="1280,720" flags="wfNoBorder" backgroundColor="#90000000">
            <eLabel name="new eLabel" position="40,40" zPosition="-2" size="1200,640" backgroundColor="#20000000" transparent="0" />
            <eLabel font="Regular; 20" foregroundColor="unffffff" backgroundColor="#20000000" halign="left" position="77,645" size="250,33" text="Cancel" transparent="1" />
            <eLabel font="Regular; 20" foregroundColor="unffffff" backgroundColor="#20000000" halign="left" position="375,645" size="250,33" text="Run" transparent="1" />
            <eLabel position="60,55" size="348,50" text="PiconsTestConverter" font="Regular; 40" valign="center" transparent="1" backgroundColor="#20000000" />
            <eLabel position="60,640" size="5,40" backgroundColor="#e61700" />
            <eLabel position="360,640" size="5,40" backgroundColor="#61e500" />
          </screen>
        """

    def __init__(self, session):
        Screen.__init__(self, session)

        self["actions"] = ActionMap(["OkCancelActions", "ShortcutActions"],
        {
            "cancel": self.cancel,
            "green": self.runScript
        }, -1)

        self.onChangedEntry = []

        self.onLayoutFinish.append(self.layoutFinished)

    def layoutFinished(self):
        pass

    def cancel(self):
        self.close()

    def runScript(self):
        self.runConvertPicons()

    '''
    Private Methods
    '''

    def getServiceList(self):
        bouquet_list = eServiceReference('1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "bouquets.tv" ORDER BY bouquet')

        serviceHandler = eServiceCenter.getInstance()
        list = serviceHandler.list(bouquet_list)

        services = self.getBouquetServices(bouquet_list)

        return services


    def slugify(self, value):
        """
        Converts to lowercase, removes non-word characters (alphanumerics and
        underscores) and converts spaces to hyphens. Also strips leading and
        trailing whitespace.

        Function is from django
        """
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
        value = re.sub('[^\w\s-]', '', value).strip().lower()
        return re.sub('[-\s]+', '-', value)


    def getBouquetServices(self, bouquet):
        services = []
        Servicelist = eServiceCenter.getInstance().list(bouquet)
        if not Servicelist is None:
            while True:
                service = Servicelist.getNext()
                if not service.valid(): #check if end of list
                    break
                if service.flags & (eServiceReference.isDirectory | eServiceReference.isMarker): #ignore non playable services
                    continue
                services.append(ServiceReference(service))
        return services

    def runConvertPicons(self):
        print "############################"
        print "## SERVICE LIST"
        print "############################"

        if os.path.isdir("/tmp/piconsTestConverter/source") is False:
            os.makedirs("/tmp/piconsTestConverter/source", 0755)

        #if os.path.isdir("/tmp/piconsTestConverter/output") is False:
        #    os.makedirs("/tmp/piconsTestConverter/output", 0755)

        services = self.getBouquetServices(eServiceReference('1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.test.tv" ORDER BY bouquet'))

        notFoundList = []

        for service in services:
            piconName = str(service).replace(":", "_")
            piconName = piconName[:-1] + ".png"

            channelName = self.slugify(unicode(service.getServiceName())) + ".png"

            piconFilePath = "/tmp/piconsTestConverter/source/" + channelName

            if os.path.isfile(piconFilePath):
                shutil.copy(piconFilePath, "/usr/share/enigma2/picon/" + piconName)
            else:
                notFoundList.append([piconFilePath, service.getServiceName(), str(service)])

        print "############################"
        print "NOT FOUND: ", notFoundList
        print "############################"
        print "## / ENDE : SERVICE LIST"
        print "############################"




