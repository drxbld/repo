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

import re, urllib, urlparse, json, threading
from resources.lib.modules import client
from resources.lib.extensions import metadata
from resources.lib.extensions import tools
from resources.lib.extensions import network
from resources.lib.externals.beautifulsoup import BeautifulSoup

class source:

	def __init__(self):
		self.pack = True # Checked by provider.py
		self.priority = 0
		self.language = ['fr']
		self.domains = ['yggtorrent.com']
		self.base_link = 'https://yggtorrent.com'
		self.search_link = '/engine/search?category=%s&subcategory=%s&q=%s&page=%s&order=desc&sort=seed'
		self.download_link = '/torrents/download/%s'
		self.category_video = 2145
		self.subcategory_any = "all"
		self.subcategories_show = {'Série TV': '2184'}
		self.subcategories_movie = {'Film': '2183', 'Animation': '2178'}

	def movie(self, imdb, title, localtitle, year):
		try:
			url = {'imdb': imdb, 'title': title, 'year': year}
			url = urllib.urlencode(url)
			return url
		except:
			return

	def tvshow(self, imdb, tvdb, tvshowtitle, localtitle, year):
		try:
			url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
			url = urllib.urlencode(url)
			return url
		except:
			return

	def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try:
			if url == None: return
			url = urlparse.parse_qs(url)
			url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
			url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
			url = urllib.urlencode(url)
			return url
		except:
			return

	def _hash(self, title, url, index):
		try:
			htmlSingle = BeautifulSoup(client.request(url))
			htmlHash = htmlSingle.find_all('td', id = 'info_hash')[0].getText()
			htmlLink = network.Container(htmlHash).torrentMagnet(title = title)
			self.tLock.acquire()
			self.tLinks[index] = htmlLink
		except:
			tools.Logger.error()
		finally:
			try: self.tLock.release()
			except: pass

	def sources(self, url, hostDict, hostprDict):
		sources = []
		try:
			if url == None:
				raise Exception()

			data = urlparse.parse_qs(url)

			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

			tools.Logger.log(data)

			title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			titleYear = '%s S%02dE%02d' % (data['tvshowtitle'], int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else '%s (%s)' % (data['title'], data['year'])

			if 'exact' in data and data['exact']:
				query = title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
				year = None
				season = None
				episode = None
				pack = False
				packCount = None
			else:
				year = int(data['year']) if 'year' in data and not data['year'] == None else None
				season = int(data['season']) if 'season' in data and not data['season'] == None else None
				episode = int(data['episode']) if 'episode' in data and not data['episode'] == None else None
				pack = data['pack'] if 'pack' in data else False
				packCount = data['packcount'] if 'packcount' in data else None

				if 'tvshowtitle' in data:
					subcategory = self.subcategories_show.values()[0] if len(self.subcategories_show) == 1 else self.subcategory_any
				else:
					subcategory = self.subcategories_movie.values()[0] if len(self.subcategories_movie) == 1 else self.subcategory_any

				if 'tvshowtitle' in data:
					if pack: query = '%s S%02d' % (title, season)
					else: query = '%s S%02dE%02d' % (title, season, episode)
				else:
					query = '%s %d' % (title, year)
				query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)
				querySplit = query.split()

			url_template = urlparse.urljoin(self.base_link, self.search_link)

			pageLimit = tools.Settings.getInteger('scraping.providers.pages')
			pageCounter = 0

			page = 0
			added = False

			timerEnd = tools.Settings.getInteger('scraping.providers.timeout') - 8
			timer = tools.Time(start = True)

			while True:
				# Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
				if timer.elapsed() > timerEnd:
					break

				pageCounter += 1
				if pageLimit > 0 and pageCounter > pageLimit:
					break

				url = url_template % (self.category_video, subcategory, urllib.quote_plus(query), page)
				html = BeautifulSoup(client.request(url))

				page += 25
				added = False

				htmlTables = html.find_all('table', 'table-striped')
				if htmlTables:
					htmlTable = htmlTables[0]
					htmlTbody = htmlTable.find_all('tbody')[0]
					htmlRows = htmlTbody.find_all('tr', recursive = False)

					self.tLock = threading.Lock()
					self.tLinks = [None] * len(htmlRows)
					htmlInfos = []
					threads = []
					for i in range(len(htmlRows)):
						htmlInfo = htmlRows[i].find_all('a', class_ = 'torrent-name', href = True)[0]
						urlHash = urllib.quote(str(htmlInfo.get('href').encode('utf-8')), ':/+')
						htmlInfos.append(htmlInfo)
						threads.append(threading.Thread(target = self._hash, args = (titleYear, urlHash, i)))

					[thread.start() for thread in threads]
					while timer.elapsed() < timerEnd and any([thread.is_alive() for thread in threads]):
						tools.Time.sleep(0.5)

					self.tLock.acquire() # Just lock in case the threads are still running.
					for i in range(len(htmlRows)):
						# Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
						if timer.elapsed() > timerEnd:
							break

						htmlRow = htmlRows[i]

						# Name
						htmlName = htmlInfos[i].getText()

						# Category
						htmlCategory = htmlRow.select('i.fa-user ~ i > a')[0].getText()
						if subcategory is self.subcategory_any:
							if 'tvshowtitle' in data and len(self.subcategories_show) > 1:
								if htmlCategory not in self.subcategories_show.keys():
									continue
							elif len(self.subcategories_show) > 1:
								if htmlCategory not in self.subcategories_movie.keys():
									continue

						# Size
						htmlSize = htmlRow.find_all('td')[3].getText()

						# Link
						htmlLink = self.tLinks[i]

						# Seeds
						htmlSeeds = int(htmlRow.find_all('td')[4].getText())

						# Metadata
						meta = metadata.Metadata(name = htmlName, title = title, year = year, season = season, episode = episode, pack = pack, packCount = packCount, link = htmlLink, size = htmlSize, seeds = htmlSeeds)
						# Ignore
						if meta.ignore(True):
							continue

						# Add
						sources.append({'url' : htmlLink, 'debridonly' : False, 'direct' : False, 'source' : 'torrent', 'language' : self.language[0], 'quality':  meta.videoQuality(), 'metadata' : meta, 'file' : htmlName})
						added = True

					self.tLock.release()
				if not added: # Last page reached with a working torrent
					break
			return sources
		except:
			tools.Logger.error()
			return sources

	def resolve(self, url):
		return url
