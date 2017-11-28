import xbmc, xbmcaddon, xbmcvfs, xbmcgui, ConfigParser, os, re, time, urllib
import requests
import shutil,urllib2
from rpc import RPC
from xbmcswift2 import Plugin
from resources.lib.formatting import *
from urlparse import urlparse
import datetime
from datetime import timedelta
import glob
import xml.etree.ElementTree as ET
############ functions ##################
def cp(ini_path):
    anyoldvar = ConfigParser.ConfigParser()
    anyoldvar.optionxform = str
    anyoldvar.read(ini_path)
    return anyoldvar

def get_tv_path(icon_name):
    addon_path = xbmcaddon.Addon().getAddonInfo("path")
    return os.path.join(addon_path, 'resources', 'img', icon_name + ".png")


def get_icon_path(id):
    return os.path.join(xbmc.translatePath('special://home/'), 'addons', id, "icon.png")


def unescape( str ):
    str = str.replace("&lt;","<")
    str = str.replace("&gt;",">")
    str = str.replace("&quot;","\"")
    str = str.replace("&amp;","&")
    str = str.replace("&nbsp;"," ")
    str = str.replace("&dash;","-")
    str = str.replace("&ndash;","-")
    return str


def sanitycheck(title, string):
    dialog = xbmcgui.Dialog()
    response = dialog.yesno(title, string)
    return response


def message(message, title='Debug'):
    dialog = xbmcgui.Dialog()
    dialog.ok(title, message)

##############################################

###################set vars ############

plugin = Plugin('iVue Creator')
big_list_view = False

namechange_path = xbmc.translatePath('special://profile/addon_data/plugin.video.IVUEcreator/namechange/')
path_to_ivue = xbmc.translatePath('special://profile/addon_data/script.ivueguide')
path_to_creator = xbmc.translatePath('special://profile/addon_data/plugin.video.IVUEcreator')

if not os.path.exists(path_to_creator):
    os.makedirs(path_to_creator)

if not os.path.exists(namechange_path):
    os.makedirs(namechange_path)

addons2_filename = xbmc.translatePath('special://profile/addon_data/script.ivueguide/addons2.ini')
addons2_ini = cp(addons2_filename)

addons_ini_path = xbmc.translatePath('special://profile/addon_data/plugin.video.IVUEcreator/addons_index.ini')
addons_index_ini = cp(addons_ini_path)

settings_xml = os.path.join(path_to_ivue, "settings.xml")
server_path = 'http://ivuetvguide.com/ivueguide/'
xml = ET.iterparse(settings_xml, events=('end',))

for event, elem in xml:
    if elem.tag == "setting":
        if elem.get("id")== "xmltv.type":
            if elem.get("value") == '6':
                channels_ini = os.path.join(path_to_creator, "custom_channels.ini")
            else:
                channels_ini = os.path.join(path_to_creator, "master_channels.ini")
                if not os.path.exists(channels_ini):
                    fp = server_path + 'master_channels.ini'
                    dp = xbmcgui.DialogProgress()
                    dp.create('Downloading ini', "working...")
                    dp.update(50)
                    xbmc.sleep(1000)
                    try:
                        file = urllib.URLopener()
                        file.retrieve(fp, channels_ini)
                        dp.update(100,'Complete.')
                        xbmc.sleep(1000)
                        dp.close()

                    except Exception as e:
                        dp.update(50, 'Error')
                        xbmc.sleep(1000)
                        dp.close()
                        message('Channels.ini download failed %s' % str(e))


#########################################

@plugin.route('/action_stream/<action>/<id>/<label>')
def action_stream(action, id, label):

    if action =='rename':

        clean_names = sorted(get_channel_names(channels_ini))
        dialog = xbmcgui.Dialog()
        new_label = dialog.select('Change '+label+' to:', clean_names)

        if new_label < 0:
            new_label = label
        else:
            new_label = clean_names[new_label]

        dialog = xbmcgui.Dialog()
        new_label = dialog.input('Enter new label', new_label, type=xbmcgui.INPUT_ALPHANUM)
        tag = ''
        count = 2
        temp_label = new_label

        while addons2_ini.has_option(id,new_label + tag):
            tag = ' (%s)' % count
            count += 1
            new_label = temp_label + tag

        if new_label == '':
            return

        addons2_ini.set(id, new_label, addons2_ini.get(id,label))
        addons2_ini.remove_option(id, label)

        with open(addons2_filename, 'wb') as configfile:
            addons2_ini.write(configfile)

        id = re.sub('\.', '-', id)
        path_to_namechange_file = os.path.join(namechange_path, id + '.ini')

        if not os.path.isfile(path_to_namechange_file):
            file = open(path_to_namechange_file, 'w')
            file.close()

        namechange_ini = cp(path_to_namechange_file)

        if not namechange_ini.has_section(id):
            namechange_ini.add_section(id)

        namechange_ini.set(id, label, new_label)

        with open(path_to_namechange_file, 'wb') as configfile:
            namechange_ini.write(configfile)

    elif action == 'revert':

        namechange_id = re.sub('\.', '-', id)
        path_to_namechange_file = os.path.join(namechange_path, namechange_id + '.ini')
        namechange_ini = cp(path_to_namechange_file)
        addon2_targ = namechange_ini.get(namechange_id,label)
        namechange_ini.remove_option(namechange_id, label)

        with open(path_to_namechange_file, 'wb') as configfile:
            namechange_ini.write(configfile)

        path = addons2_ini.get(id, addon2_targ)
        addons2_ini.set(id, label, path )
        addons2_ini.remove_option(id, addon2_targ)

        with open(addons2_filename, 'wb') as configfile:
            addons2_ini.write(configfile)

    elif action == 'enable':

        if addons2_ini.has_section(id):
            path = addons2_ini.get(id, label)
            addons2_ini.remove_option(id, label)

            if len(addons2_ini.items(id)) == 0:
                addons2_ini.remove_section(id)

        id = re.sub('-blacklist', '', id)
        addons2_ini.set(id, label, path)

        with open(addons2_filename, 'wb') as configfile:
            addons2_ini.write(configfile)

        message('stream enabled', 'Done')

    elif action == 'disable':

        if not addons2_ini.has_section(id + '-blacklist'):
            addons2_ini.add_section(id + '-blacklist')

        path = addons2_ini.get(id, label)
        addons2_ini.remove_option(id, label)
        addons2_ini.set(id + '-blacklist', label, path)

        with open(addons2_filename, 'wb') as configfile:
            addons2_ini.write(configfile)

        message('stream disabled', 'Done')

    xbmc.executebuiltin('Container.Refresh')


@plugin.route('/addon/<id>')
def addon(id):

    ite = addons2_ini.items(id)

    try:
        namechange_id = re.sub('\.', '-', id)
        path_to_namechange_file = os.path.join(namechange_path, namechange_id + '.ini')
        namechange_ini = cp(path_to_namechange_file)
        namechange_items = namechange_ini.items(namechange_id)

    except Exception as e:
        namechange_items = ''

    items = []
    clean_names = sorted(get_channel_names(channels_ini))

    try:

        for name, url in sorted(ite, key=lambda s: s[0].lower()):
            context_items = []
            relabelled = ''

            if namechange_items is not '':
                for namechange_item in namechange_items:
                    if name == namechange_item[1]:
                        relabelled = namechange_item[0]
                        break

            context_items.append(("%s" % 'Rename',
                                  'XBMC.RunPlugin(%s)' % (
                                      plugin.url_for(action_stream, action='rename', id=id, label=name))))
            if relabelled is not '':
                context_items.append(("%s" % 'Revert to original label',
                                      'XBMC.RunPlugin(%s)' % (
                                          plugin.url_for(action_stream, action='revert', id=id, label=relabelled))))
            if addons2_ini.has_option(id,name) and '-blacklist' in id:
                context_items.append(("%s" % 'Enable',
                              'XBMC.RunPlugin(%s)' % (
                              plugin.url_for(action_stream, action='enable', id=id, label=name))))
            else:
                context_items.append(("%s" % 'Disable',
                                  'XBMC.RunPlugin(%s)' % (
                                      plugin.url_for(action_stream, action='disable', id=id, label=name))))

            matched = 0
            for clean_name in clean_names:

                if name.lower() == clean_name.lower():
                    fancy_label = "[COLOR green]%s[/COLOR] " % clean_name
                    matched = 1

            if not matched:
                fancy_label = name
            if relabelled is not '':
                fancy_label = '(R) ' + fancy_label
            items.append(
            {
                'label': fancy_label,
                'path': url,
                'icon': get_icon_path(id),
                'context_menu': context_items,
                'thumbnail': get_icon_path(id),
                'is_playable': True,
            })
    except Exception as e:
        pass
    return items


@plugin.route('/player')
def player():

    sections = addons2_ini.sections()
    items = []
    for section in sections:

        if section == 'plugin.video.IVUEcreator':
            fancy_label = 'M3U Playlist'
        elif section == 'script.ivueguide':
            fancy_label = 'PVR Playlist'
        else:
             fancy_label = section

        items.append(
        {
            'label': fancy_label,
            'path': plugin.url_for('addon', id=section),
            'thumbnail': get_icon_path(section),
        })

    return items


@plugin.route('/pvr_subscribe')
def pvr_subscribe():
    plugin.set_setting("pvr.subscribe", "true")
    update('script.ivueguide',True,'')
    xbmc.executebuiltin('Container.Refresh')


@plugin.route('/pvr_unsubscribe')
def pvr_unsubscribe():
    plugin.set_setting("pvr.subscribe", "false")
    remove_addon('script.ivueguide')
    xbmc.executebuiltin('Container.Refresh')


@plugin.route('/play/<url>')
def play(url):
    xbmc.executebuiltin('PlayMedia(%s)' % url)


@plugin.route('/add_folder/<id>/<path>/<label>')
def add_folder(id, path, label):

    if addons_index_ini.has_section(id) == False:
        addons_index_ini.add_section(id)

    addons_index_ini.set(id, remove_tags(label).strip(), path)

    with open(addons_ini_path, 'wb') as configfile:
        addons_index_ini.write(configfile)

    ret = update(id, False, label)
    xbmc.executebuiltin('Container.Refresh')


@plugin.route('/delete_folder/<id>/<path>/<label>')
def delete_folder(id, path, label):

    if sanitycheck('Delete ' + str(label), 'Are you sure?'):

        if addons_index_ini.has_section(id):
            items = addons_index_ini.items(id)
            for item in items:
                if item[1] == path:
                    addons_index_ini.remove_option(id, item[0])

        with open(addons_ini_path, 'wb') as configfile:
            addons_index_ini.write(configfile)

        message('deleted %s use update single addon to update .ini' % label, 'Done!')
        xbmc.executebuiltin('Container.Refresh')

    return False


@plugin.route('/clear')
def clear():
    storagePath = xbmc.translatePath('special://profile/addon_data/plugin.video.IVUEcreator/.storage')
    namechange_path = xbmc.translatePath('special://profile/addon_data/plugin.video.IVUEcreator/namechange')

    if sanitycheck('Clear all subs?', 'are you sure?'):

        if os.path.exists(addons2_filename):
            os.remove(addons2_filename)
        if os.path.exists(addons_ini_path):
            os.remove(addons_ini_path)
        if os.path.exists(storagePath):
            shutil.rmtree(storagePath)

        if sanitycheck('IVUEcreator','Delete all namechange ini\'s?'):
            if os.path.exists(namechange_path):
                shutil.rmtree(namechange_path)
                os.makedirs(namechange_path)

        remove_channels_ini()
        plugin.set_setting("pvr.subscribe", "false")
        message('Delete addons', 'Done')


@plugin.route('/remove_addon/<id>')
def remove_addon(id):
    nc_id = re.sub('\.','-',id)
    storagePath = xbmc.translatePath('special://profile/addon_data/plugin.video.IVUEcreator/.storage/%s' % id)
    namechange_path = xbmc.translatePath('special://profile/addon_data/plugin.video.IVUEcreator/namechange/%s' % nc_id +'.ini')
    path = "plugin://%s" % id

    if id == 'script.ivueguide':
        fancy_label = 'PVR Playlist'
    elif id == 'plugin.video.IVUEcreator':
        fancy_label = 'M3U Playlist'
    else:
        fancy_label = id

    if sanitycheck('Clear ' + str(fancy_label), 'Are you sure?'):

        if addons_index_ini.has_section(id):
            addons_index_ini.remove_section(id)

        with open(addons_ini_path, 'wb') as configfile:
            addons_index_ini.write(configfile)

        if addons2_ini.has_section(id):
            addons2_ini.remove_section(id)
        if addons2_ini.has_section(id+'-blacklist'):
            addons2_ini.remove_section(id+'-blacklist')

        with open(addons2_filename, 'wb') as configfile:
            addons2_ini.write(configfile)

        if os.path.exists(storagePath):
            os.remove(storagePath)

        if os.path.exists(namechange_path):
            if sanitycheck('IVUEcreator','Delete %s \'s namechange ini?' % fancy_label):
                os.remove(namechange_path)

        message('Done', 'Cleared ' + str(fancy_label))

    xbmc.executebuiltin('Container.Refresh')


@plugin.route('/deleteaddon')
def deleteaddon():

    sections = addons_index_ini.sections()
    items = []
    for section in sections:
        items.append(
            {
                'label': section,
                'path': plugin.url_for('remove_addon', id=section),
                'thumbnail': get_icon_path(section),

            })
    return items

@plugin.route('/update_addon/<id>')
def update_addon(id):
    update(id)
    xbmc.executebuiltin('Container.Refresh')


@plugin.route('/updateaddon')
def updateaddon():

    sections = addons_index_ini.sections()

    if len(sections) < 1:
        message('No addons detected', 'IVUEcreator')
        return

    items = []
    for section in sections:
        items.append(
            {
                'label': section,
                'path': plugin.url_for('update_addon', id=section),
                'thumbnail': get_icon_path(section),
            })
    return items


@plugin.route('/folder/<id>/<path>')
def folder(id, path):

    folders = []

    if addons_index_ini.has_section(id):
        items = addons_index_ini.items(id)
        for item in items:
            folders.append(item[1])

    try:
        response = RPC.files.get_directory(media="files", directory=path, properties=["thumbnail"])
        files = response["files"]
    except Exception as e:
        message(str(e))
        return

    dirs = dict([[remove_tags(f["label"]), f["file"]] for f in files if f["filetype"] == "directory"])
    links = {}
    thumbnails = {}
    for f in files:
        if f["filetype"] == "file":
            label = f["label"]
            file = f["file"]
            while (label in links):
                label = "%s." % label
            links[label] = file
            thumbnails[label] = f["thumbnail"]

    items = []

    for label in sorted(dirs):
        path = dirs[label]
        context_items = []
        if path in folders:
            fancy_label = "[COLOR yellow]%s[/COLOR] " % remove_tags(label)
            context_items.append(("[COLOR yellow]%s[/COLOR] " % 'Unsubscribe', 'XBMC.RunPlugin(%s)' % (
            plugin.url_for(delete_folder, id=id, path=path, label=fancy_label))))
        else:
            fancy_label = "%s" % remove_tags(label)
            context_items.append(("[COLOR yellow]%s[/COLOR] " % 'Subscribe', 'XBMC.RunPlugin(%s)' % (
            plugin.url_for(add_folder, id=id, path=path, label=fancy_label))))
        items.append(
            {
                'label': fancy_label,
                'path': plugin.url_for('folder', id=id, path=path),
                'thumbnail': get_icon_path(id),
                'context_menu': context_items,
            })

    for label in sorted(links):
        items.append(
            {
                'label': label,
                'path': plugin.url_for('play', url=links[label]),
                'thumbnail': thumbnails[label],
            })
    return items


@plugin.route('/subscribe')
def subscribe():

    sections = addons_index_ini.sections()

    ids = {}
    for folder in sections:
        id = folder
        ids[id] = id
    all_addons = []
    for type in ["xbmc.addon.video", "xbmc.addon.audio"]:
        response = RPC.addons.get_addons(type=type, properties=["name", "thumbnail"])
        if "addons" in response:
            found_addons = response["addons"]
            all_addons = all_addons + found_addons

    seen = set()
    addons = []
    for addon in all_addons:
        if addon['addonid'] not in seen:
            addons.append(addon)
        seen.add(addon['addonid'])

    items = []

    pvr = plugin.get_setting('pvr.subscribe')
    context_items = []
    label = "PVR"
    if pvr == "true":
        fancy_label = "[COLOR yellow]%s[/COLOR] " % remove_tags(label)
        context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Unsubscribe', 'XBMC.RunPlugin(%s)' % (plugin.url_for(pvr_unsubscribe))))
    else:
        fancy_label = "%s" % remove_tags(label)
        context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Subscribe', 'XBMC.RunPlugin(%s)' % (plugin.url_for(pvr_subscribe))))
    items.append(
    {
        'label': fancy_label,
        'path': plugin.url_for('pvr'),
        'thumbnail':get_icon_path(''),
        'context_menu': context_items,
    })

    addons = sorted(addons, key=lambda addon: remove_tags(addon['name']).lower().strip())
    for addon in addons:
        label = addon['name']

        id = addon['addonid']

        path = "plugin://%s" % id

        context_items = []
        if id in ids:
            fancy_label = "[COLOR yellow]%s[/COLOR] " % remove_tags(label)
            context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Unsubscribe',
                                  'XBMC.RunPlugin(%s)' % (plugin.url_for(remove_addon, id=id))))
        else:
            fancy_label = "%s" % remove_tags(label)
            context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Subscribe', 'XBMC.RunPlugin(%s)' % (
            plugin.url_for(add_folder, id=id, path=path, label=fancy_label))))
        items.append(
            {
                'label': fancy_label,
                'path': plugin.url_for('folder', id=id, path=path),
                'thumbnail': get_icon_path(id),
                'context_menu': context_items,
            })
    return items


@plugin.route('/update')
def update(id = '',silent = True, ini_label = ''):

    if id == '' and silent == False:
        if not sanitycheck('Update all addons?', 'Depending on your setup, this may take a while!'):
            return

    start = time.time()
    update_set, streams = {}, {}

    dp = xbmcgui.DialogProgress()
    dp.create('Updating links', "working...")
    dp.update(25)

    if id =='script.ivueguide':
        if plugin.get_setting("pvr.subscribe") == "true":
            streams["script.ivueguide"] = {}
            items = pvr()
            num_of_addons =+ 1
            for item in items:
                name = item["label"]
                url = item["path"]
                streams["script.ivueguide"][name] = url
    else:

        if id is not '':
            sections = [id]
            num_of_addons = 1
        else:
            sections = addons_index_ini.sections()
            num_of_addons = len(sections)

        if num_of_addons < 1:

            message('No addons detected!','IVUEcreator')
            return

        for section in sections:
            dp.update(30, 'Gathering ' + str(section) + '\'s streams, ' + str(num_of_addons) + ' of ' + str(
                len(sections)) + ' to go')
            items = addons_index_ini.items(section)

            for item in items:
                path = item[1]
                id = section

                if not id in streams:
                    streams[id] = {}

                try:
                    response = RPC.files.get_directory(media="files", directory=path, properties=["thumbnail"])
                    files = response["files"]

                except Exception as e:
                    message('Error: unable to retrieve links from this folder.', str(e))
                    #delete the addons ini entry

                    addons_index_ini.remove_option(id, item[0])

                    with open(addons_ini_path, 'wb') as configfile:
                        addons_index_ini.write(configfile)
                    break #?
                    #return False


                poss_streams, poss_dirs = 0, 0
                links, thumbnails= {},{}

                for f in files:

                    if f['filetype'] == 'file':
                        poss_streams += 1
                    elif f['filetype'] == 'directory':
                        poss_dirs += 1

                    label = f["label"]
                    file = f["file"]

                    while (label in links):
                        label = "%s." % label

                    links[label] = file
                    thumbnails[label] = f["thumbnail"]
                    streams[id][label] = file

                if ini_label == item[0] and silent == False:

                    if not sanitycheck('Subscribe to ' + id, 'There are ' + str(poss_streams) + ' streams and \n ' + str(
                            poss_dirs) + ' directorys in ' + item[0] + ', are you sure?'):

                        dp.update(45, 'carrying on....')
                        if addons_index_ini.has_section(id):
                            addons_index_ini.remove_option(id, item[0])

                        with open(addons_ini_path, 'wb') as configfile:
                            addons_index_ini.write(configfile)

                        break

            num_of_addons -= 1

    dp.update(50, 'links retrieved....')

    dp.update(60, 'getting channel labels....')

    clean_names = get_clean_names(channels_ini)
    num_of_addons = len(streams)
    stream_count = 0

    for id in sorted(streams):
        dp.update(75, 'Processing ' + id + ' links, ' + str(num_of_addons) + ' addons to go. ' + str(
            stream_count) + ' links added...')

        if addons2_ini.has_section(id):
            addons2_ini.remove_section(id)

        addons2_ini.add_section(id)

        if id not in update_set:
            update_set[id] = {}

        channels = streams[id]
        for channel in sorted(channels):

            url = channels[channel].strip()
            label = channel.strip()
            label = remove_formatting(label, clean_names, id)

            #if config.has_option(id + '-blacklist', temp_label.strip()) and config.get(id + '-blacklist', temp_label.strip()) == url:
            #    label = '<nolabel>'

            if '<nolabel>' not in label:

                ncid = re.sub('\.', '-', id)
                path_to_namechange_file = os.path.join(namechange_path, ncid + '.ini')
                namechange_config = ConfigParser.ConfigParser()
                namechange_config.optionxform = str
                namechange_config.read(path_to_namechange_file)

                if namechange_config.has_option(ncid, label):

                    label = namechange_config.get(ncid, label)

                if label not in update_set[id]:
                    update_set[id][label] = []

                update_set[id][label].append(url)
                stream_count += 1

        num_of_addons -= 1

    dp.update(90, 'writing links to .ini....')

    for id in sorted(update_set):
        for label in sorted(update_set[id]):
            num_of_streams = len(update_set[id][label])
            if num_of_streams > 1:
                count = 1
                for url in update_set[id][label]:
                    if count == 1:
                        addons2_ini.set(id, label, url)
                    else:
                        addons2_ini.set(id, label + ' (' + str(count) + ')', url)
                    count += 1
            else:
                addons2_ini.set(id, label, update_set[id][label][0])

    with open(addons2_filename, 'wb') as configfile:
        addons2_ini.write(configfile)

    dp.update(100)
    dp.close()
    m, s = divmod((time.time() - start), 60)
    h, m = divmod(m, 60)
    if ( xbmcgui.getCurrentWindowId() == 10025 ):
        message(str(stream_count) + ' streams added from ' + str(len(streams)) + ' addons in ' + "%02d mins, %02d secs" % (m, s), 'Done!')    
    else:    
        xbmc.executebuiltin('RunScript(script.ivueguide, run)')


@plugin.route('/search/<what>')
def search(what):

    if not what:
        return

    what = re.sub(' ', '', what.lower())
    items = []
    sections = addons2_ini.sections()

    for section in sections:
        options = addons2_ini.items(section)

        for option in options:

            name = re.sub(' ', '', option[0].lower())

            if what in name:

                items.append({
                    "label": "[COLOR green]%s [%s][/COLOR]" % (section, option[0]),
                    "path": option[1],
                    "is_playable": True,
                })

    return items

@plugin.route('/pvr')
def pvr():
    index = 0
    urls = []
    channels = {}
    for group in ["radio","tv"]:
        urls = urls + xbmcvfs.listdir("pvr://channels/%s/All channels/" % group)[1]
    for group in ["radio","tv"]:
        groupid = "all%s" % group
        json_query = RPC.PVR.get_channels(channelgroupid=groupid, properties=[ "thumbnail", "channeltype", "hidden", "locked", "channel", "lastplayed", "broadcastnow" ] )
        if "channels" in json_query:
            for channel in json_query["channels"]:
                channelname = channel["label"]
                channelid = channel["channelid"]-1
                channellogo = channel['thumbnail']
                streamUrl = urls[index]
                index = index + 1
                url = "pvr://channels/%s/All channels/%s" % (group,streamUrl)
                channels[url] = channelname
    items = []
    for url in sorted(channels, key=lambda x: channels[x]):
        name = channels[url]
        items.append(
        {
            'label': name,
            'path': url,
            'is_playable': True,
        })
    return items
@plugin.route('/search_dialog')
def search_dialog():
    dialog = xbmcgui.Dialog()
    what = dialog.input("Search")
    if what:
        return search(what)

@plugin.route('/error_log')
def error_log():
    path_to_log = xbmc.translatePath(os.path.join('special://logpath/','kodi.log'))
    try:
        f = open(path_to_log)
        lines = f.read()
    except Exception as e:
        message('unable to open kodi.log: '+str(e),'Error')
        return
    xbmc.executebuiltin("ActivateWindow(10147)")
    controller = xbmcgui.Window(10147)
    xbmc.sleep(500)
    controller.getControl(1).setLabel('Error log')
    controller.getControl(5).setText(str(lines))
    return False


@plugin.route('/addm3u')
def addm3u():
    items =[]
    addon = 'plugin.video.IVUEcreator'
    items.append(
        {
            'label': "Add m3u file  (Some links may require f4mtester)",
            'path': plugin.url_for('add_m3u'),
            'thumbnail': get_icon_path('tv'),
        })
    items.append(
        {
            'label': "Delete m3u playlist",
            'path': plugin.url_for('remove_addon', id=addon),
            'thumbnail': get_icon_path('tv'),
        })
    return items


@plugin.route('/add_m3u')
def add_m3u():

    addon_path_userdata = xbmc.translatePath('special://profile/addon_data/plugin.video.IVUEcreator/')
    addon = 'plugin.video.IVUEcreator'
    pre_txt = "plugin://plugin.video.f4mTester/?url="
    clean_names = get_clean_names(channels_ini)

    channels = {'name': list(),
                'path': list(), }
    dialog = xbmcgui.Dialog()
    download_file = dialog.yesno('iVue Creator', 'm3u File Location', yeslabel='Url', nolabel='local drives')
    default = 'http path to file'

    dp = xbmcgui.DialogProgress()
    dp.create('Retrieving m3u playlist', "working...")
    dp.update(25)

    if download_file:

        try:
            http_path_to_m3u = dialog.input('Enter path to .m3u', default, type=xbmcgui.INPUT_ALPHANUM)
            dp.update(40, 'attempting http download')
            file = urllib.URLopener()
            m3u_file = file.retrieve(http_path_to_m3u, os.path.join(addon_path_userdata, "m3u.m3u"))
            m3u_file = m3u_file[0]

        except Exception as e:
            download_file = 0
            dp.update(40, 'Download failed with Error s%.... \n select local file' % e)
            xbmc.sleep(1000)

    if not download_file:
        m3u_file = xbmcgui.Dialog().browse(1, "Select m3u", "files")
        dp.update(40, 'attempting local file read')

    if not m3u_file:
        message('No m3u file chosen', 'Error')
        dp.close()
        return

    dp.update(60, 'playlist loaded, processing...')

        # better file handling here, along with better dupe filename support, just a general re-write really
    with open(m3u_file) as fp:
        for line in fp:
            if "#EXTM3U" not in line:

                if "#EXTINF:" in line:
                    title = line.rsplit(',', 1)[1]
                    title = remove_formatting(title.strip(), clean_names, addon)

                    channels['name'].append(title)

                elif "http" in line[0:4]:
                    path = line[:-1]
                    post_txt = '&name=' + title + '&streamtype=TSDOWNLOADER|'
                    if '.ts' in path:
                        channels['path'].append(pre_txt + path + post_txt)
                    else:
                        channels['path'].append(path)

                else:
                    message("What the hell is this?")
                    return False

    dp.update(80, 'Writing to file...')


    if not addons2_ini.has_section(addon):
       # addons2_ini.remove_section(addon)

        addons2_ini.add_section(addon)

    count = 0
    for ii in range(0, len(channels['name'])):

        if addons2_ini.has_option(addon, channels["name"][ii]):
            channel = str(channels["name"][ii]) + ' ' + str(count)
            if '<nolabel>' not in channel:
                addons2_ini.set(addon, channel, channels["path"][ii])
                count += 1
        else:
            if '<nolabel>' not in channels["name"][ii]:
                addons2_ini.set(addon, channels["name"][ii], channels["path"][ii])

    with open(addons2_filename, 'wb') as configfile:
        addons2_ini.write(configfile)
    dp.update(100, 'all done...')


@plugin.route('/remove_channels_ini')
def remove_channels_ini():
    path_to_creator = xbmc.translatePath('special://profile/addon_data/plugin.video.IVUEcreator')
    channels_ini = os.path.join(path_to_creator, "master_channels.ini")
    if os.path.exists(channels_ini):
        if sanitycheck('IVUEcreator','Update channels.ini?'):
            os.remove(channels_ini)
            message('IVUEcreator','Done!!')
    else:
        message('No channels.ini to update?!')

    xbmc.executebuiltin('Container.Refresh')


@plugin.route('/')
def index():
    items, context_items = [],[]

    context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Update channels INI',
                          'XBMC.RunPlugin(%s)' % (plugin.url_for(remove_channels_ini))))
    items.append(
        {
            'label': "Subscribe",
            'path': plugin.url_for('subscribe'),
            'thumbnail': get_tv_path('tv'),
            'context_menu': context_items,
        })
    items.append(
        {
            'label': "Add/Delete m3u(s)",
            'path': plugin.url_for('addm3u'),
            'thumbnail': get_tv_path('tv'),
            'context_menu': context_items,
        })
    items.append(
        {
            'label': "Play",
            'path': plugin.url_for('player'),
            'thumbnail': get_tv_path('tv'),
            'context_menu': context_items,
        })
    items.append(
        {
            'label': "Search",
            'path': plugin.url_for('search_dialog'),
            'thumbnail': get_tv_path('tv'),
            'context_menu': context_items,
        })
    items.append(
        {
            'label': "Update single addon",
            'path': plugin.url_for('updateaddon'),
            'thumbnail': get_tv_path('tv'),
            'context_menu': context_items,
        })
    items.append(
        {
            'label': "Update all addons",
            'path': plugin.url_for('update'),
            'thumbnail': get_tv_path('tv'),
            'context_menu': context_items,
        })
    items.append(
        {
            'label': "Clear single addon",
            'path': plugin.url_for('deleteaddon'),
            'thumbnail': get_tv_path('tv'),
            'context_menu': context_items,
        })
    items.append(
        {
            'label': "Start over",
            'path': plugin.url_for('clear'),
            'thumbnail': get_tv_path('tv'),
            'context_menu': context_items,
        })
    items.append(
        {
            'label': "Error log",
            'path': plugin.url_for('error_log'),
            'thumbnail': get_tv_path('tv'),
            'context_menu': context_items,
        })
    return items

if __name__ == '__main__':
    plugin.run()





