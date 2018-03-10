# -*- coding: utf-8 -*-

'''
	Gaia Add-on
	Copyright (C) 2016 Gaia

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import urlparse
import sys
from resources.lib.extensions import tools

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))

action = params.get('action')
name = params.get('name')
title = params.get('title')
year = params.get('year')
imdb = params.get('imdb')
tmdb = params.get('tmdb')
tvdb = params.get('tvdb')
season = params.get('season')
episode = params.get('episode')
tvshowtitle = params.get('tvshowtitle')
premiered = params.get('premiered')
url = params.get('url')
link = params.get('link')
image = params.get('image')
meta = params.get('meta')
select = params.get('select')
query = params.get('query')
content = params.get('content')

type = params.get('type')

kids = params.get('kids')
kids = 0 if kids == None or kids == '' else int(kids)

source = params.get('source')
if not source == None:
	source = tools.Converter.dictionary(source)
	if isinstance(source, list):
		source = source[0]

metadata = params.get('metadata')
if not metadata == None:
	metadata = tools.Converter.dictionary(metadata)

# LEAVE THIS HERE. Can be used by downloadsList for updating the directory list automatically in a thread.
# Stops downloader directory Updates
#if not action == 'download' and not (action == 'downloadsList' and not params.get('status') == None):
#	from resources.lib.extensions import downloader
#	downloader.Downloader.itemsStop()

# Always check, not only on the main menu (action == None), since skin widgets also call the addon.
tools.System.observe()

#tools.System.initialize()

# Execute on first launch.
if action == None:
	tools.System.launch()

if action == None or action == 'home':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).root()

elif action == 'movieNavigator':
	from resources.lib.indexers import navigator
	lite = tools.Converter.boolean(params.get('lite'))
	navigator.navigator(type = type, kids = kids).movies(lite = lite)

elif action == 'movieFavouritesNavigator':
	from resources.lib.indexers import navigator
	lite = tools.Converter.boolean(params.get('lite'))
	navigator.navigator(type = type, kids = kids).movieFavourites(lite = lite)

elif action == 'tvNavigator':
	from resources.lib.indexers import navigator
	lite = tools.Converter.boolean(params.get('lite'))
	navigator.navigator(type = type, kids = kids).tvshows(lite = lite)

elif action == 'tvFavouritesNavigator':
	from resources.lib.indexers import navigator
	lite = tools.Converter.boolean(params.get('lite'))
	navigator.navigator(type = type, kids = kids).tvFavourites(lite = lite)

elif action == 'toolsNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).tools()

elif action == 'searchNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).search()

elif action == 'clearAll':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).clearAll()

elif action == 'clearProviders':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).clearProviders()

elif action == 'clearWebcache':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).clearWebcache()

elif action == 'clearHistory':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).clearHistory()

elif action == 'clearShortcuts':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).clearShortcuts()

elif action == 'clearSearches':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).clearSearches()

elif action == 'clearDownloads':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).clearDownloads()

elif action == 'clearTemporary':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).clearTemporary()

elif action == 'clearViews':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).clearViews()

elif action == 'person':
	from resources.lib.indexers import movies
	movies.movies(type = type, kids = kids).person(params.get('terms'))

elif action == 'movies':
	from resources.lib.indexers import movies
	movies.movies(type = type, kids = kids).get(url)

elif action == 'moviePage':
	from resources.lib.indexers import movies
	movies.movies(type = type, kids = kids).get(url)

elif action == 'movieArrivals':
	from resources.lib.indexers import movies
	movies.movies(type = type, kids = kids).arrivals()

elif action == 'movieSearch':
	from resources.lib.indexers import movies
	movies.movies(type = type, kids = kids).search(params.get('terms'))

elif action == 'moviePerson':
	from resources.lib.indexers import movies
	movies.movies(type = type, kids = kids).person(params.get('terms'))

elif action == 'movieCollections':
	from resources.lib.indexers import movies
	movies.movies(type = type, kids = kids).collections()

elif action == 'movieGenres':
	from resources.lib.indexers import movies
	movies.movies(type = type, kids = kids).genres()

elif action == 'movieLanguages':
	from resources.lib.indexers import movies
	movies.movies(type = type, kids = kids).languages()

elif action == 'movieCertificates':
	from resources.lib.indexers import movies
	movies.movies(type = type, kids = kids).certifications()

elif action == 'movieAge':
	from resources.lib.indexers import movies
	movies.movies(type = type, kids = kids).age()

elif action == 'movieYears':
	from resources.lib.indexers import movies
	movies.movies(type = type, kids = kids).years()

elif action == 'moviePersons':
	from resources.lib.indexers import movies
	movies.movies(type = type, kids = kids).persons(url)

elif action == 'movieUserlists':
	from resources.lib.indexers import movies
	movies.movies(type = type, kids = kids).userlists(mode = params.get('mode'))

elif action == 'channels':
	from resources.lib.indexers import channels
	channels.channels(type = type, kids = kids).get()

elif action == 'tvshows':
	from resources.lib.indexers import tvshows
	tvshows.tvshows(type = type, kids = kids).get(url)

elif action == 'tvshowPage':
	from resources.lib.indexers import tvshows
	tvshows.tvshows(type = type, kids = kids).get(url)

elif action == 'tvSearch':
	from resources.lib.indexers import tvshows
	tvshows.tvshows(type = type, kids = kids).search(params.get('terms'))

elif action == 'tvPerson':
	from resources.lib.indexers import tvshows
	tvshows.tvshows(type = type, kids = kids).person(params.get('terms'))

elif action == 'tvGenres':
	from resources.lib.indexers import tvshows
	tvshows.tvshows(type = type, kids = kids).genres()

elif action == 'tvNetworks':
	from resources.lib.indexers import tvshows
	tvshows.tvshows(type = type, kids = kids).networks()

elif action == 'tvCertificates':
	from resources.lib.indexers import tvshows
	tvshows.tvshows(type = type, kids = kids).certifications()

elif action == 'tvAge':
	from resources.lib.indexers import tvshows
	tvshows.tvshows(type = type, kids = kids).age()

elif action == 'tvPersons':
	from resources.lib.indexers import tvshows
	tvshows.tvshows(type = type, kids = kids).persons(url)

elif action == 'tvUserlists':
	from resources.lib.indexers import tvshows
	tvshows.tvshows(type = type, kids = kids).userlists(mode = params.get('mode'))

elif action == 'seasons':
	from resources.lib.indexers import seasons
	seasons.seasons(type = type, kids = kids).get(tvshowtitle, year, imdb, tvdb)

elif action == 'episodes':
	from resources.lib.indexers import episodes
	episodes.episodes(type = type, kids = kids).get(tvshowtitle, year, imdb, tvdb, season, episode)

elif action == 'calendar':
	from resources.lib.indexers import episodes
	episodes.episodes(type = type, kids = kids).calendar(url)

elif action == 'tvHome':
	from resources.lib.indexers import episodes
	episodes.episodes(type = type, kids = kids).home()

elif action == 'tvArrivals':
	from resources.lib.indexers import episodes
	episodes.episodes(type = type, kids = kids).arrivals()

elif action == 'tvCalendars':
	from resources.lib.indexers import episodes
	episodes.episodes(type = type, kids = kids).calendars()

elif action == 'episodeUserlists':
	from resources.lib.indexers import episodes
	episodes.episodes(type = type, kids = kids).userlists()

elif action == 'seasonUserlists':
	from resources.lib.indexers import seasons
	seasons.seasons(type = type, kids = kids).userlists()

elif action == 'seasonList':
	from resources.lib.indexers import seasons
	seasons.seasons(type = type, kids = kids).seasonList(url)

elif action == 'refresh':
	from resources.lib.modules import control
	control.refresh()

elif action == 'queueItem':
	from resources.lib.modules import control
	control.queueItem()

elif action == 'addView':
	from resources.lib.modules import views
	views.addView(content)

elif action == 'moviePlaycount':
	from resources.lib.modules import playcount
	playcount.movies(imdb, query)

elif action == 'episodePlaycount':
	from resources.lib.modules import playcount
	playcount.episodes(imdb, tvdb, season, episode, query)

elif action == 'tvPlaycount':
	from resources.lib.modules import playcount
	playcount.tvshows(name, imdb, tvdb, season, query)

elif action == 'trailer':
	from resources.lib.modules import trailer
	trailer.trailer().play(name, url)

elif action == 'play':
	from resources.lib.extensions import core
	from resources.lib.extensions import interface
	interface.Loader.show() # Already show herte, since getConstants can take long when retrieving debrid service list.
	preset = params.get('preset')
	try: seasoncount = int(params.get('seasoncount'))
	except: seasoncount = None
	core.Core(type = type, kids = kids).play(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select, preset = preset, seasoncount = seasoncount)

elif action == 'playExact':
	from resources.lib.extensions import core
	terms = params.get('terms')
	core.Core(type = type, kids = kids).playExact(terms)

elif action == 'addItem':
	from resources.lib.extensions import core
	core.Core(type = type, kids = kids).addItem()

elif action == 'playItem':
	from resources.lib.extensions import interface
	from resources.lib.extensions import core
	interface.Loader.show() # Immediately show the loader, since slow system will take long to show it in playItem().
	downloadType = params.get('downloadType')
	downloadId = params.get('downloadId')
	handleMode = params.get('handleMode')
	core.Core(type = type, kids = kids).playItem(source = source, metadata = metadata, downloadType = downloadType, downloadId = downloadId, handleMode = handleMode)

elif action == 'playLocal':
	from resources.lib.extensions import core
	path = params.get('path')
	downloadType = params.get('downloadType')
	downloadId = params.get('downloadId')
	core.Core(type = type, kids = kids).playLocal(path = path, source = source, metadata = metadata, downloadType = downloadType, downloadId = downloadId)

elif action == 'alterSources':
	from resources.lib.extensions import core
	from resources.lib.extensions import interface
	interface.Loader.show()
	core.Core(type = type, kids = kids).alterSources(url)

# [GAIACODE]

elif action == 'presetSources':
	from resources.lib.extensions import core
	from resources.lib.extensions import interface
	interface.Loader.show()
	core.Core(type = type, kids = kids).presetSources(url)

elif action == 'systemNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).systemNavigator()

elif action == 'systemInformation':
	tools.System.information()

elif action == 'systemManager':
	tools.System.manager()

elif action == 'systemClean':
	tools.System.clean()

elif action == 'informationNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).informationNavigator()

elif action == 'informationPremium':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).informationPremium()

elif action == 'informationSplash':
	from resources.lib.extensions import interface
	interface.Splash.popupFull()

elif action == 'informationChangelog':
	from resources.lib.extensions import interface
	interface.Changelog.show()

elif action == 'informationAnnouncement':
	tools.Announcements.show(True)

elif action == 'informationAbout':
	from resources.lib.extensions import interface
	interface.Splash.popupAbout()

elif action == 'openLink':
	link = params.get('link')
	tools.System.openLink(link)

elif action == 'copyLink':
	from resources.lib.extensions import interface
	from resources.lib.extensions import clipboard
	from resources.lib.extensions import network
	try:
		interface.Loader.show() # Needs some time to load. Show busy.
		if 'link' in params:
			link = params.get('link')
		elif 'source' in params:
			link = source['url']
			if 'resolve' in params:
				resolve = params.get('resolve')
				if resolve:
					if 'urlresolved' in source:
						link = source['urlresolved']
					else:
						link = network.Networker().resolve(source, clean = True, resolve = resolve)
			if not link: # Sometimes resolving does not work. Eg: 404 errors.
				link = source['url']
			link = network.Networker(link).link() # Clean link
		clipboard.Clipboard.copyLink(link, True)
	except:
		pass
	interface.Loader.hide()

elif action == 'copyClipboard':
	from resources.lib.extensions import interface
	from resources.lib.extensions import clipboard
	try:
		interface.Loader.show() # Needs some time to load. Show busy.
		clipboard.Clipboard.copy(params.get('value'), True)
	except:
		pass
	interface.Loader.hide()

elif action == 'showDetails':
	from resources.lib.extensions import metadata as metadatax
	from resources.lib.extensions import interface
	try:
		interface.Loader.show() # Needs some time to load. Show busy.
		metadatax.Metadata.showDialog(source = source, metadata = metadata)
	except:
		pass
	interface.Loader.hide()

elif action == 'verificationProviders':
	from resources.lib.extensions import verification
	verification.Verification().verifyProviders()

elif action == 'verificationAccounts':
	from resources.lib.extensions import verification
	verification.Verification().verifyAccounts()

elif action == 'verificationNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).verificationNavigator()

elif action == 'favouritesNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).favouritesNavigator()

elif action == 'arrivalsNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).arrivalsNavigator()

elif action == 'clearNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).clearNavigator()

elif action == 'traktmoviesNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).traktmovies()

elif action == 'traktmovieslistsNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).traktmovieslists()

elif action == 'imdbmoviesNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).imdbmovies()

elif action == 'trakttvNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).trakttv()

elif action == 'trakttvlistsNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).trakttvlists()

elif action == 'imdbtvNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).imdbtv()

elif action == 'moviesCategories':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).moviesCategories()

elif action == 'moviesLists':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).moviesLists()

elif action == 'moviesPeople':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).moviesPeople()

elif action == 'moviesSearchNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).moviesSearchNavigator()

elif action == 'tvCategories':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).tvCategories()

elif action == 'tvLists':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).tvLists()

elif action == 'tvPeople':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).tvPeople()

elif action == 'tvSearchNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).tvSearchNavigator()

elif action == 'tvYears':
	from resources.lib.indexers import tvshows
	tvshows.tvshows().years()

elif action == 'tvLanguages':
	from resources.lib.indexers import tvshows
	tvshows.tvshows().languages()

elif action == 'searchExact':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).searchExact()

elif action == 'searchRecent':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).searchRecent()

elif action == 'searchRecentMovies':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).searchRecentMovies()

elif action == 'searchRecentShows':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).searchRecentShows()

elif action == 'cacheItem':
	from resources.lib.extensions import core
	handleMode = params.get('handleMode')
	core.Core(type = type, kids = kids).cacheItem(source = source, metadata = metadata, handleMode = handleMode)

####################################################
# PROVIDERS
####################################################

elif action == 'providersNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).providersNavigator()

elif action == 'providersSettings':
	tools.Settings.launch(category = tools.Settings.CategoryProviders)

elif action == 'providersSort':
	from resources.lib.extensions import provider
	mode = params.get('mode')
	slot = params.get('slot')
	provider.Provider.sortDialog(mode = mode, slot = slot)

elif action == 'providersPreset':
	from resources.lib.extensions import provider
	slot = params.get('slot')
	provider.Provider.presetDialog(slot = slot)

elif action == 'providersOptimization':
	from resources.lib.extensions import provider
	settings = params.get('settings')
	provider.Provider().optimization(settings = settings)

elif action == 'providersCustomization':
	from resources.lib.extensions import provider
	settings = params.get('settings')
	provider.Provider().customization(settings = settings)

####################################################
# ACCOUNTS
####################################################

elif action == 'accountsNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).accountsNavigator()

elif action == 'accountsSettings':
	tools.Settings.launch(category = tools.Settings.CategoryAccounts)

####################################################
# DOWNLOADS
####################################################

elif action == 'download':
	try:
		from resources.lib.extensions import core
		from resources.lib.extensions import downloader
		from resources.lib.extensions import interface
		interface.Loader.show()
		downloadType = params.get('downloadType')
		downloadId = params.get('downloadId')
		refresh = tools.Converter.boolean(params.get('refresh'))
		downer = downloader.Downloader(downloadType)
		if downloadId == None:
			image = params.get('image')
			handleMode = params.get('handleMode')
			link = core.Core(type = type, kids = kids).sourcesResolve(source, info = True, internal = False, download = True, handleMode = handleMode)['link']
			if link == None:
				interface.Loader.hide()
			else:
				title = tools.Media.title(type = type, metadata = metadata)
				downer.download(media = type, title = title, link = link, image = image, metadata = metadata, source = source, refresh = refresh)
		else:
			downer.download(id = downloadId, forceAction = True, refresh = refresh)
	except:
		interface.Loader.hide()
		tools.Logger.error()

elif action == 'downloadDetails':
	from resources.lib.extensions import downloader
	downloadType = params.get('downloadType')
	downloadId = params.get('downloadId')
	downloader.Downloader(type = downloadType, id = downloadId).details()

elif action == 'downloads':
	from resources.lib.indexers import navigator
	downloadType = params.get('downloadType')
	navigator.navigator(type = type, kids = kids).downloads(downloadType)

elif action == 'downloadsManager':
	from resources.lib.extensions import downloader
	downer = downloader.Downloader(downloader.Downloader.TypeManual)
	downer.items(status = downloader.Downloader.StatusAll, refresh = False)

elif action == 'downloadsBrowse':
	from resources.lib.indexers import navigator
	downloadType = params.get('downloadType')
	downloadError = params.get('downloadError')
	navigator.navigator(type = type, kids = kids).downloadsBrowse(downloadType, downloadError)

elif action == 'downloadsList':
	downloadType = params.get('downloadType')
	downloadStatus = params.get('downloadStatus')
	if downloadStatus == None:
		from resources.lib.indexers import navigator
		navigator.navigator(type = type, kids = kids).downloadsList(downloadType)
	else:
		from resources.lib.extensions import downloader
		downer = downloader.Downloader(downloadType)
		# Do not refresh the list using a thread. Seems like the thread is not always stopped and then it ends with multiple threads updating the list.
		# During the update duration multiple refreshes sometimes happen due to this. Hence, you will see the loader flash multiple times during the 10 secs.
		# Also, with a fresh the front progress dialog also flashes and reset it's focus.
		#downer.items(status = status, refresh = True)
		downer.items(status = downloadStatus, refresh = False)

elif action == 'downloadsClear':
	downloadType = params.get('downloadType')
	downloadStatus = params.get('downloadStatus')
	if downloadStatus == None:
		from resources.lib.indexers import navigator
		navigator.navigator(type = type, kids = kids).downloadsClear(downloadType)
	else:
		from resources.lib.extensions import downloader
		downer = downloader.Downloader(downloadType)
		downer.clear(status = downloadStatus)

elif action == 'downloadsRefresh':
	from resources.lib.extensions import downloader
	downloadType = params.get('downloadType')
	downer = downloader.Downloader(downloadType)
	downer.itemsRefresh()

elif action == 'downloadsSettings':
	from resources.lib.modules import control
	tools.Settings.launch(category = tools.Settings.CategoryDownloads)

####################################################
# LIGHTPACK
####################################################

elif action == 'lightpackNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).lightpackNavigator()

elif action == 'lightpackSwitchOn':
	tools.Lightpack().switchOn(message = True)

elif action == 'lightpackSwitchOff':
	tools.Lightpack().switchOff(message = True)

elif action == 'lightpackAnimate':
	force = params.get('force')
	force = True if force == None else tools.Converter.boolean(force)
	tools.Lightpack().animate(force = force, message = True, delay = True)

elif action == 'lightpackSettings':
	tools.Lightpack().settings()

####################################################
# KIDS
####################################################

elif action == 'kidsLock':
	tools.Kids.lock()

elif action == 'kidsUnlock':
	tools.Kids.unlock()

elif action == 'kidsNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).kidsNavigator()

####################################################
# DOCUMENTARIES
####################################################

elif action == 'documentariesNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = tools.Media.TypeDocumentary, kids = kids).movies()

####################################################
# SHORTS
####################################################

elif action == 'shortsNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = tools.Media.TypeShort, kids = kids).movies()

####################################################
# SERVICES
####################################################

elif action == 'servicesNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).servicesNavigator()

####################################################
# PREMIUMIZE
####################################################

elif action == 'premiumizeNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).premiumizeNavigator()

elif action == 'premiumizeDownloadsNavigator':
	from resources.lib.indexers import navigator
	lite = tools.Converter.boolean(params.get('lite'))
	navigator.navigator(type = type, kids = kids).premiumizeDownloadsNavigator(lite = lite)

elif action == 'premiumizeList':
	from resources.lib.extensions import debrid
	debrid.PremiumizeInterface().directoryList()

elif action == 'premiumizeListAction':
	from resources.lib.extensions import debrid
	item = params.get('item')
	context = params.get('context')
	debrid.PremiumizeInterface().directoryListAction(item, context)

elif action == 'premiumizeItem':
	from resources.lib.extensions import debrid
	item = params.get('item')
	debrid.PremiumizeInterface().directoryItem(item)

elif action == 'premiumizeItemAction':
	from resources.lib.extensions import debrid
	item = params.get('item')
	debrid.PremiumizeInterface().directoryItemAction(item)

elif action == 'premiumizeAdd':
	from resources.lib.extensions import debrid
	debrid.PremiumizeInterface().addManual()

elif action == 'premiumizeInformation':
	from resources.lib.extensions import debrid
	debrid.PremiumizeInterface().downloadInformation()

elif action == 'premiumizeAccount':
	from resources.lib.extensions import debrid
	debrid.PremiumizeInterface().account()

elif action == 'premiumizeWebsite':
	from resources.lib.extensions import debrid
	debrid.Premiumize().website(open = True)

elif action == 'premiumizeVpn':
	from resources.lib.extensions import debrid
	debrid.Premiumize().vpn(open = True)

elif action == 'premiumizeClear':
	from resources.lib.extensions import debrid
	debrid.PremiumizeInterface().clear()

elif action == 'premiumizeSettings':
	tools.Settings.launch(category = tools.Settings.CategoryAccounts)

####################################################
# PREMIUMIZE
####################################################

elif action == 'offcloudNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).offcloudNavigator()

elif action == 'offcloudDownloadsNavigator':
	from resources.lib.indexers import navigator
	lite = tools.Converter.boolean(params.get('lite'))
	category = params.get('category')
	navigator.navigator(type = type, kids = kids).offcloudDownloadsNavigator(lite = lite, category = category)

elif action == 'offcloudList':
	from resources.lib.extensions import debrid
	category = params.get('category')
	debrid.OffCloudInterface().directoryList(category = category)

elif action == 'offcloudListAction':
	from resources.lib.extensions import debrid
	item = params.get('item')
	context = params.get('context')
	debrid.OffCloudInterface().directoryListAction(item = item, context = context)

elif action == 'poffcloudItem':
	from resources.lib.extensions import debrid
	item = params.get('item')
	debrid.OffCloudInterface().directoryItem(item)

elif action == 'offcloudItemAction':
	from resources.lib.extensions import debrid
	item = params.get('item')
	debrid.OffCloudInterface().directoryItemAction(item)

elif action == 'offcloudAdd':
	from resources.lib.extensions import debrid
	category = params.get('category')
	debrid.OffCloudInterface().addManual(category = category)

elif action == 'offcloudInformation':
	from resources.lib.extensions import debrid
	category = params.get('category')
	debrid.OffCloudInterface().downloadInformation(category = category)

elif action == 'offcloudAdd':
	from resources.lib.extensions import debrid
	debrid.OffCloudInterface().addManual()

elif action == 'offcloudAccount':
	from resources.lib.extensions import debrid
	debrid.OffCloudInterface().account()

elif action == 'offcloudWebsite':
	from resources.lib.extensions import debrid
	debrid.OffCloud().website(open = True)

elif action == 'offcloudClear':
	from resources.lib.extensions import debrid
	category = params.get('category')
	debrid.OffCloudInterface().clear(category = category)

elif action == 'offcloudSettings':
	tools.Settings.launch(category = tools.Settings.CategoryAccounts)

elif action == 'offcloudSettingsLocation':
	from resources.lib.extensions import debrid
	debrid.OffCloudInterface().settingsLocation()

####################################################
# REALDEBRID
####################################################

elif action == 'realdebridAuthentication':
	from resources.lib.extensions import debrid
	debrid.RealDebridInterface().accountAuthentication()

elif action == 'realdebridNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).realdebridNavigator()

elif action == 'realdebridDownloadsNavigator':
	from resources.lib.indexers import navigator
	lite = tools.Converter.boolean(params.get('lite'))
	navigator.navigator(type = type, kids = kids).realdebridDownloadsNavigator(lite = lite)

elif action == 'realdebridList':
	from resources.lib.extensions import debrid
	debrid.RealDebridInterface().directoryList()

elif action == 'realdebridListAction':
	from resources.lib.extensions import debrid
	item = params.get('item')
	debrid.RealDebridInterface().directoryListAction(item)

elif action == 'realdebridAdd':
	from resources.lib.extensions import debrid
	debrid.RealDebridInterface().addManual()

elif action == 'realdebridInformation':
	from resources.lib.extensions import debrid
	debrid.RealDebridInterface().downloadInformation()

elif action == 'realdebridAccount':
	from resources.lib.extensions import debrid
	debrid.RealDebridInterface().account()

elif action == 'realdebridWebsite':
	from resources.lib.extensions import debrid
	debrid.RealDebrid().website(open = True)

elif action == 'realdebridClear':
	from resources.lib.extensions import debrid
	debrid.RealDebridInterface().clear()

elif action == 'realdebridSettings':
	tools.Settings.launch(category = tools.Settings.CategoryAccounts)

####################################################
# EASYNEWS
####################################################

elif action == 'easynewsNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).easynewsNavigator()

elif action == 'easynewsAccount':
	from resources.lib.extensions import debrid
	debrid.EasyNewsInterface().account()

elif action == 'easynewsWebsite':
	from resources.lib.extensions import debrid
	debrid.EasyNews().website(open = True)

elif action == 'easynewsVpn':
	from resources.lib.extensions import debrid
	debrid.EasyNews().vpn(open = True)

elif action == 'easynewsSettings':
	tools.Settings.launch(category = tools.Settings.CategoryAccounts)

####################################################
# QUASAR
####################################################

elif action == 'quasarNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).quasarNavigator()

elif action == 'quasarConnect':
	tools.Quasar.connect(confirm = True)

elif action == 'quasarInstall':
	tools.Quasar.install()

elif action == 'quasarLaunch':
	tools.Quasar.launch()

elif action == 'quasarInterface':
	tools.Quasar.interface()

elif action == 'quasarSettings':
	tools.Quasar.settings()

####################################################
# URLRESOLVER
####################################################

elif action == 'urlresolverNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).urlresolverNavigator()

elif action == 'urlresolverSettings':
	tools.UrlResolver.settings()

elif action == 'urlresolverInstall':
	tools.UrlResolver.enable(refresh = True)

####################################################
# NOOBSANDNERDS
####################################################

elif action == 'noobsandnerdsNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).noobsandnerdsNavigator()

elif action == 'noobsandnerdsSettings':
	tools.NoobsAndNerds.settings()

elif action == 'noobsandnerdsInstall':
	tools.NoobsAndNerds.enable(refresh = True)

####################################################
# YOUTUBE
####################################################

elif action == 'youtubeNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).youtubeNavigator()

elif action == 'youtubeSettings':
	tools.YouTube.settings()

elif action == 'youtubeInstall':
	tools.YouTube.enable()

elif action == 'youtubeLaunch':
	tools.YouTube.launch()

elif action == 'youtubeWebsite':
	tools.YouTube.website(open = True)

####################################################
# METAHANDLER
####################################################

elif action == 'metahandlerNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).metahandlerNavigator()

elif action == 'metahandlerSettings':
	tools.MetaHandler.settings()

elif action == 'metahandlerInstall':
	tools.MetaHandler.enable(refresh = True)

####################################################
# SPEEDTEST
####################################################

elif action == 'speedtestNavigator':
	from resources.lib.indexers import navigator
	from resources.lib.extensions import speedtest
	speedtest.SpeedTester.participation()
	navigator.navigator().speedtestNavigator()

elif action == 'speedtest':
	from resources.lib.extensions import speedtest
	speedtest.SpeedTester.select(params.get('update'))

elif action == 'speedtestGlobal':
	from resources.lib.extensions import speedtest
	speedtest.SpeedTesterGlobal().show(params.get('update'))

elif action == 'speedtestPremiumize':
	from resources.lib.extensions import speedtest
	speedtest.SpeedTesterPremiumize().show(params.get('update'))

elif action == 'speedtestOffCloud':
	from resources.lib.extensions import speedtest
	speedtest.SpeedTesterOffCloud().show(params.get('update'))

elif action == 'speedtestRealDebrid':
	from resources.lib.extensions import speedtest
	speedtest.SpeedTesterRealDebrid().show(params.get('update'))

elif action == 'speedtestEasyNews':
	from resources.lib.extensions import speedtest
	speedtest.SpeedTesterEasyNews().show(params.get('update'))

elif action == 'speedtestParticipation':
	from resources.lib.extensions import speedtest
	speedtest.SpeedTester.participation(force = True)

elif action == 'speedtestComparison':
	from resources.lib.extensions import speedtest
	speedtest.SpeedTester.comparison()

####################################################
# LOTTERY
####################################################

elif action == 'lotteryVoucher':
	from resources.lib.extensions import api
	api.Api.lotteryVoucher()

####################################################
# VIEWS
####################################################

elif action == 'viewsNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).viewsNavigator()

elif action == 'viewsCategoriesNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).viewsCategoriesNavigator()

elif action == 'views':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).views(content = params.get('content'))

####################################################
# HISTORY
####################################################

elif action == 'historyNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).historyNavigator()

elif action == 'historyType':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).historyType()

elif action == 'historyStream':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).historyStream()

####################################################
# TRAKT
####################################################

elif action == 'traktManager':
	from resources.lib.modules import trakt
	refresh = params.get('refresh')
	if refresh == None: refresh = True
	else: refresh = tools.Converter.boolean(refresh)
	trakt.manager(imdb = imdb, tvdb = tvdb, season = season, episode = episode, refresh = refresh)

elif action == 'traktAuthorize':
	from resources.lib.modules import trakt
	trakt.authTrakt()

elif action == 'traktListAdd':
	from resources.lib.modules import trakt
	trakt.listAdd()

elif action == 'traktNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).traktNavigator()

elif action == 'traktSettings':
	tools.Trakt.settings()

elif action == 'traktInstall':
	tools.Trakt.enable()

elif action == 'traktLaunch':
	tools.Trakt.launch()

elif action == 'traktWebsite':
	tools.Trakt.website(open = True)

####################################################
# NETWORK
####################################################

elif action == 'networkNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).networkNavigator()

elif action == 'networkInformation':
	from resources.lib.extensions import network
	network.Networker.informationDialog()

####################################################
# VPN
####################################################

elif action == 'vpnNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).vpnNavigator()

elif action == 'vpnVerification':
	from resources.lib.extensions import vpn
	settings = tools.Converter.boolean(params.get('settings'))
	vpn.Vpn().verification(settings = settings)

elif action == 'vpnConfiguration':
	from resources.lib.extensions import vpn
	settings = tools.Converter.boolean(params.get('settings'))
	vpn.Vpn().configuration(settings = settings)

elif action == 'vpnSettings':
	from resources.lib.extensions import vpn
	vpn.Vpn().settings()

elif action == 'vpnLaunch':
	from resources.lib.extensions import vpn
	execution = params.get('execution')
	vpn.Vpn().launch(execution = execution)

####################################################
# EXTENSIONS
####################################################

elif action == 'extensions':
	id = params.get('id')
	tools.Extensions.dialog(id = id)

elif action == 'extensionsNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).extensionsNavigator()

elif action == 'extensionsAvailableNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).extensionsAvailableNavigator()

elif action == 'extensionsInstalledNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).extensionsInstalledNavigator()

####################################################
# THEME
####################################################

elif action == 'themeSkinSelect':
	from resources.lib.extensions import interface
	interface.Skin.select()

elif action == 'themeIconSelect':
	from resources.lib.extensions import interface
	interface.Icon.select()

####################################################
# BACKUP
####################################################

elif action == 'backupNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).backupNavigator()

elif action == 'backupAutomatic':
	tools.Backup.automatic()

elif action == 'backupImport':
	tools.Backup.manualImport()

elif action == 'backupExport':
	tools.Backup.manualExport()

####################################################
# SETTINGS
####################################################

elif action == 'settings':
	from resources.lib.extensions import settings
	settings.Selection().show()

elif action == 'settingsAdvanced':
	from resources.lib.extensions import settings
	settings.Advanced().show()

elif action == 'settingsWizard':
	from resources.lib.extensions import settings
	settings.Wizard().show()

elif action == 'settingsExternal':
	tools.Settings.externalSave(params)

elif action == 'settingsCustomReleases':
	tools.Settings.customSetReleases(type = type)

elif action == 'settingsCustomUploaders':
	tools.Settings.customSetUploaders(type = type)

elif action == 'settingsColor':
	from resources.lib.extensions import interface
	interface.Format.settingsColorUpdate(type = type)

elif action == 'settingsAlluc':
	from resources.lib.extensions import settings
	settings.Alluc.apiShow()

####################################################
# DONATIONS
####################################################

elif action == 'donationsNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).donationsNavigator()

elif action == 'donationsCrypto':
	from resources.lib.extensions import tools
	currency = params.get('currency')
	tools.Donations.show(currency = currency)

elif action == 'donationsOther':
	from resources.lib.extensions import tools
	tools.Donations.other()

####################################################
# LEGAL
####################################################

elif action == 'legalDisclaimer':
	from resources.lib.extensions import interface
	interface.Legal.show(exit = True)

####################################################
# SHORTCUTS
####################################################

elif action == 'shortcutsShow':
	from resources.lib.extensions import shortcuts
	location = params.get('location')
	id = params.get('id')
	link = params.get('link')
	name = params.get('name')
	create = tools.Converter.boolean(params.get('create'))
	delete = tools.Converter.boolean(params.get('delete'))
	shortcuts.Shortcuts().show(location = location, id = id, link = link, name = name, create = create, delete = delete)

elif action == 'shortcutsNavigator':
	from resources.lib.indexers import navigator
	location = params.get('location')
	navigator.navigator(type = type, kids = kids).shortcutsNavigator(location = location)

elif action == 'shortcutsOpen':
	from resources.lib.extensions import shortcuts
	location = params.get('location')
	id = params.get('id')
	shortcuts.Shortcuts().open(location = location, id = id)

####################################################
# LIBRARY
####################################################

elif action == 'libraryNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).libraryNavigator()

elif action == 'libraryLocalNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).libraryLocalNavigator()

elif action == 'libraryBrowseNavigator':
	from resources.lib.indexers import navigator
	error = tools.Converter.boolean(params.get('error'))
	navigator.navigator(type = type, kids = kids).libraryBrowseNavigator(error = error)

elif action == 'libraryAdd':
	from resources.lib.extensions import library
	calendar = tools.Converter.boolean(params.get('calendar'))
	metadata = params.get('metadata')
	library.Library(type = type, kids = kids).add(link = link, title = title, year = year, imdb = imdb, tmdb = tmdb, tvdb = tvdb, metadata = metadata)

elif action == 'libraryUpdate':
	from resources.lib.extensions import library
	library.Library.update()

elif action == 'libraryService':
	from resources.lib.extensions import library
	library.Library.service(background = False)

elif action == 'libraryLocal':
	from resources.lib.extensions import library
	library.Library(type = type).local()

elif action == 'librarySettings':
	from resources.lib.extensions import library
	library.Library.settings()

####################################################
# ORION
####################################################

elif action == 'orionNavigator':
	from resources.lib.indexers import navigator
	navigator.navigator(type = type, kids = kids).orionNavigator()
