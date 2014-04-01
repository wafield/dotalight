import MySQLdb
import json
import webapi
import datetime

HOST     = 'localhost'
USER     = 'dotalight'
DATABASE = 'dotalight'

def upgrade_tables():
    conn = MySQLdb.connect(host=HOST, user=USER, db=DATABASE)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS players')
    c.execute('DROP TABLE IF EXISTS matches')
    conn.commit()
    conn.close()
    init_tables()
    return

def init_tables():
    conn = MySQLdb.connect(host=HOST, user=USER, db=DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS players 
                 (steamid BIGINT UNSIGNED PRIMARY KEY, pname TEXT, avatar TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS matches
                 (matchid INT UNSIGNED, accountid INT UNSIGNED, 
                  start_time BIGINT UNSIGNED, lobby_type TINYINT UNSIGNED, 
                  game_mode TINYINT UNSIGNED, duration SMALLINT UNSIGNED,
                  win TINYINT UNSIGNED, 
                  player_slot TINYINT UNSIGNED, hero_id SMALLINT UNSIGNED, 
                  kills TINYINT UNSIGNED, deaths TINYINT UNSIGNED, 
                  assists TINYINT UNSIGNED, lasthits SMALLINT UNSIGNED,
                  denies SMALLINT UNSIGNED, gold SMALLINT UNSIGNED,
                  gold_pm SMALLINT UNSIGNED, xp_pm SMALLINT UNSIGNED,
                  gold_spent SMALLINT UNSIGNED, level TINYINT UNSIGNED,
                  PRIMARY KEY (matchid, accountid))''')
    conn.commit()
    conn.close()
    return

    
def connect_db():
    db = MySQLdb.connect(host=HOST, user=USER, db=DATABASE, charset='utf8')
    return db


def get_player_summaries(steamids, db=None):
    if db is None:
        conn = connect_db()
    else:
        conn = db
    c = conn.cursor()
    success = []
    for pid in steamids:
        c.execute('SELECT * FROM players WHERE pid=%s', (pid))
        row = c.fetchone()
        if not row is None:
            success.append(row[0])
    c.close()
    if db is None:
        conn.close()
    return success
    
def insert_player_summaries(js, db=None):
    pinfo = json.loads(js)['response']['players']
    if db is None:
        conn = connect_db()
    else:
        conn = db
    c = conn.cursor()
    success = []
    for p in pinfo:
        fail = False
        try:
            c.execute('INSERT INTO players VALUES (%s, "%s", "%s")',
                      (p['steamid'], p['personaname'], p['avatarmedium']))
        except Exception:
            fail = True
        if not fail:
            success.append(p['steamid'])
    c.close()
    conn.commit()
    if db is None:
        conn.close()
    return success

def is_player_recorded(steamid, db=None):
    if db is None:
        conn = connect_db()
    else:
        conn = db
    c = conn.cursor()
    ret = False
    c.execute('SELECT steamid FROM players where steamid = %s', (steamid))
    if c.fetchone():
        ret = True
    c.close()
    if db is None:
        conn.close()
    return ret

def get_last_match_for_player(accountid, db=None):
    if db is None:
        conn = connect_db()
    else:
        conn = db
    c = conn.cursor()
    c.execute('SELECT max(*) FROM matches where accountid = %s', (accountid))
    ret = c.fetchone()
    c.close()
    if db is None:
        conn.close()
    return ret[0]

def get_num_matches_for_player(accountid, db=None):
    if db is None:
        conn = connect_db()
    else:
        conn = db
    c = conn.cursor()
    c.execute('SELECT count(*) FROM matches where accountid = %s', (accountid))
    ret = c.fetchone()
    c.close()
    if db is None:
        conn.close()
    return ret[0]

def insert_match(js, accountid, db=None):
    details = json.loads(js)['result']
    players = details['players']
    our_player = None
    for player in players:
        if player['account_id'] == accountid:
            our_player = player
            break
    
    if our_player is None:
        return False
    
    matchid    = details['match_id']
    start_time = details['start_time']
    lobby_type = details['lobby_type']
    game_mode  = details['game_mode']
    duration   = details['duration']
    win        = details['radiant_win']

    p_slot     = player['player_slot']
    hero_id    = player['hero_id']
    kills      = player['kills']
    deaths     = player['deaths']
    assists    = player['assists']
    last_hits   = player['last_hits']
    denies     = player['denies']
    gold       = player['gold']
    gold_pm    = player['gold_per_min']
    xp_pm      = player['xp_per_min']
    gold_spent = player['gold_spent']
    level      = player['level']

    value = (matchid, accountid, start_time, 
             lobby_type, game_mode, duration, win,
             p_slot, hero_id, kills, deaths,
             assists, last_hits, denies, gold,
             gold_pm, xp_pm, gold_spent, level)

    insert_sql = 'INSERT INTO matches VALUES (%s)' % ('%s,' * (len(value)-1) + '%s')
    
    if db is None:
        conn = connect_db()
    else:
        conn = db
    c = conn.cursor()
    c.execute(insert_sql, value)
    c.close()
    conn.commit()
    if db is None:
        conn.close()
    return True

