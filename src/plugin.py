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

from Plugins.Plugin import PluginDescriptor

from PiconsTestConverterView import PiconsTestConverterView

#############################################################

def main(session, **kwargs):
	session.open(PiconsTestConverterView)

def Plugins(**kwargs):
	pluginList = [
		PluginDescriptor(name="PiconsTestConverter", description=_("Convert Picons from channel-name.png to channel-key.png"), where = PluginDescriptor.WHERE_PLUGINMENU, icon="plugin.png", fnc=main, needsRestart = False)
	]
	return pluginList
