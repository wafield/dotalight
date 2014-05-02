import urllib2
import jinja2

KEY = '2B15A41E6B172A5ED773904A8689AB6E'

URL_STEAMAPI = 'http://api.steampowered.com'

URL_ResolveVanityURL = URL_STEAMAPI + \
    '/ISteamUser/ResolveVanityURL/v0001/' + \
    '?key=' + KEY + \
    '&vanityurl='

URL_GetPlayerSummaries = URL_STEAMAPI + \
    '/ISteamUser/GetPlayerSummaries/v0002/' + \
    '?key=' + KEY + \
    '&steamids='

MatchHistoryOptions = [
    'hero_id',
    'game_mode',
    'account_id',
    'start_at_match_id',
    'matches_requested'
    ]

URL_GetMatchHistory = jinja2.Template(
    URL_STEAMAPI + \
    '/IDOTA2Match_570/GetMatchHistory/V001/' + \
    '?key=' + KEY + \
    ''.join([opt.join(['{% if ',' is defined %}&','={{ ',' }}{% endif %}']) 
        for opt in MatchHistoryOptions])
)

URL_GetMatchDetails = \
    URL_STEAMAPI + \
    '/IDOTA2Match_570/GetMatchDetails/V001/' + \
    '?key=' + KEY + \
    '&match_id='

URL_GetHeroes = \
    URL_STEAMAPI + \
    '/IEconDOTA2_570/GetHeroes/V001' + \
    '?key=' + KEY

def get_player_steamid(vanityurl):
    request = URL_ResolveVanityURL + vanityurl
    response = urllib2.urlopen(request)
    json = response.read()
    response.close()
    return json

def get_player_summaries(steamids):
    request = URL_GetPlayerSummaries + ','.join([str(id) for id in steamids])
    response = urllib2.urlopen(request)
    json = response.read()
    response.close()
    return json

def get_match_details(match_id):
    request = URL_GetMatchDetails + str(match_id)
    response = urllib2.urlopen(request)
    json = response.read()
    response.close()
    return json


def get_match_histories(**kwargs):
    request = URL_GetMatchHistory.render(**kwargs)
    response = urllib2.urlopen(request)
    json = response.read()
    response.close()
    return json

def get_heroes():
    response = urllib2.urlopen(URL_GetHeroes)
    json = response.read()
    response.close()
    return json

def id64to32(steamid):
    # return steamid - 76561197960265728L
    return steamid & 0xffffffff
