import database
import webapi
import json
import html
import jinja2

CSET = 'utf8'

def update_player_profile(vanityurl):
    db = database.connect_db()
    response = json.loads(webapi.get_player_steamid(vanityurl))['response']
    if response['success'] != 1:
        return (False,)
    steamid = int(response['steamid'])

    if not database.is_player_recorded(steamid, db):
        js = webapi.get_player_summaries([steamid])
        if not database.insert_player_summaries(js, db):
            return (False,)

    accountid = webapi.id64to32(steamid)
    first_request = 25
    n_stored = database.get_num_matches_for_player(accountid, db)
    js = webapi.get_match_histories(account_id=accountid,
                                    matches_requested=first_request)
    minfo = json.loads(js)['result']
    if minfo['status'] != 1:
        return (False,)
    n_total = minfo['total_results']
    n_return = minfo['num_results']

    n = n_total - n_stored

    if n < 0:
        return (False,)
    elif n == 0:
        return (True, steamid)

    if n <= n_return:
        matches = minfo['matches'][:n]
    else:
        matches = minfo['matches']

    for match in matches:
        matchid = match['match_id']
        js = webapi.get_match_details(matchid)
        success = database.insert_match(js, accountid, db)
        if not success:
            return (False,)

    n = n - n_return
    last_match_id = matches[-1]['match_id']

    while n > 0:
        matches_requested = 99 if n > 99 else n
        js = webapi.get_match_histories(account_id=accountid,
                                        start_at_match_id=last_match_id,
                                        matches_requested=matches_requested+1)
        minfo = json.loads(js)['result']
        if minfo['status'] != 1:
            return (False,)
        matches = minfo['matches'][1:]
        for match in matches:
            matchid = match['match_id']
            js = webapi.get_match_details(matchid)
            success = database.insert_match(js, accountid, db)
            if not success:
                return (False,)
        n = n - matches_requested
        last_match_id = matches[-1]['match_id']
    db.close()
    return (True, steamid);

def render_dashboard(steamid, service=0, heroid=0):
    if service == 0 or service == 1:
        pp = database.get_player_summaries([steamid])
        if len(pp) == 0:
            error_msg = 'Player with steamid %d deos no exist!' % (steamid)
            return html.HTML['error'].render(error_msg=error_msg).encode(CSET)
        pp = pp[0]
        pname = pp[1].encode(CSET)
        pavatar = pp[2]
        matches = database.get_matches_for_player(steamid, heroid)
        match_table = html.HTML['match_table'].render(matches=matches).encode(CSET)
        if service == 1:
            return match_table
        else:
            return html.HTML['dashboard'].render(player_name=pname,
                                                 player_avatar=pavatar,
                                                 match_table=match_table).encode(CSET)
    elif service == 2:
        items = [('kills', 'Kills'), ('deaths', 'Deaths'), ('assists', 'Assists')] 
        return render_chart(steamid, heroid, items, 'Kills/Deaths/Assists')
    elif service == 3:
        items = [('lasthits', 'Last Hits'), ('denies', 'Denies')]
        return render_chart(steamid, heroid, items, 'Last Hits/Denies')
    elif service == 4:
        items = [('glod_pm', 'Gold Per Min'), ('xp_pm', 'Exp Per Min')]
        return render_chart(steamid, heroid, items, 'Gold/Experience Per Minute')
    else:
        error_msg = "Bad request!"
        return html.HTML['error'].render(error_msg=error_msg).encode(CSET)

def render_chart(steamid, heroid, items, title):
    matches = database.get_matches_for_player(steamid, heroid)
    if len(matches) >= 10:
        matches = matches[:10] #get last ten games
    matches.reverse()
    return html.HTML['match_chart'].render(matches=matches, items=items, title=title).encode(CSET)
