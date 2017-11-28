import xbmcaddon, base64

Decode = base64.decodestring
MainBase = (Decode('aHR0cDovL3B5cmFtaWQudGVhbXp0LnNlZWRyLmlvL3B5cmFtaWQvaG9tZS50eHQ='))
addon = xbmcaddon.Addon('plugin.video.thepyramid')