import time
import os
import xbmc
import xbmcgui
import xbmcaddon

databasePath = xbmc.translatePath('special://profile/addon_data/plugin.video.IVUEcreator')
d = xbmcgui.Dialog()

for root, dirs, files in os.walk(databasePath,topdown=True):
	dirs[:] = [d for d in dirs]
	for name in files:
		if "plugin.video" in name:
			try:
				os.remove(os.path.join(root,name))
			except: 
				d = xbmcgui.Dialog()
				d.ok('Ivuecreator', 'Error Removing ' + str(name),'','[COLOR yellow]Thank you for using Ivuecreator[/COLOR]')
				pass
		else:
			continue
			
for root, dirs, files in os.walk(databasePath,topdown=True):
	dirs[:] = [d for d in dirs]
	for name in files:
		if "addons" in name:
			try:
				os.remove(os.path.join(root,name))
			except: 
				d = xbmcgui.Dialog()
				d.ok('Ivuecreator', 'Error Removing ' + str(name),'','[COLOR yellow]Thank you for using Ivuecreator[/COLOR]')
				pass
		else:
			continue
			
for root, dirs, files in os.walk(databasePath,topdown=True):
	dirs[:] = [d for d in dirs]
	for name in files:
		if "folders" in name:
			try:
				os.remove(os.path.join(root,name))
			except: 
				d = xbmcgui.Dialog()
				d.ok('Ivuecreator', 'Error Removing ' + str(name),'','[COLOR yellow]Thank you for using Ivuecreator[/COLOR]')
				pass
		else:
			continue

d = xbmcgui.Dialog()			
d.ok('Ivue creator', 'Please restart for ','the changes to take effect','[COLOR yellow]Thank you for using Ivuecreator[/COLOR]')
