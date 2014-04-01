import database
import webapi
import json
import time

def update_player_profile(vanityurl):
    db = database.connect_db()
    response = json.loads(webapi.get_player_steamid(vanityurl))['response']
    if response['success'] != 1:
        return False
    steamid = int(response['steamid'])

    if not database.is_player_recorded(steamid, db):
        js = webapi.get_player_summaries([steamid])
        if not database.insert_player_summaries(js, db):
            return False

    accountid = webapi.id64to32(steamid)
    first_request = 25
    n_stored = database.get_num_matches_for_player(accountid, db)
    js = webapi.get_match_histories(account_id=accountid,
                                    matches_requested=first_request)
    minfo = json.loads(js)['result']
    if minfo['status'] != 1:
        return False
    n_total = minfo['total_results']
    n_return = minfo['num_results']

    n = n_total - n_stored

    if n < 0:
        return False
    elif n == 0:
        return True

    if n <= n_return:
        matches = minfo['matches'][:n]
    else:
        matches = minfo['matches']

    for match in matches:
        matchid = match['match_id']
        js = webapi.get_match_details(matchid)
        success = database.insert_match(js, accountid, db)
        if not success:
            return False

    n = n - n_return
    last_match_id = matches[-1]['match_id']

    while n > 0:
        matches_requested = 99 if n > 99 else n
        js = webapi.get_match_histories(account_id=accountid,
                                        start_at_match_id=last_match_id,
                                        matches_requested=matches_requested+1)
        minfo = json.loads(js)['result']
        if minfo['status'] != 1:
            return False
        matches = minfo['matches'][1:]
        for match in matches:
            matchid = match['match_id']
            js = webapi.get_match_details(matchid)
            success = database.insert_match(js, accountid, db)
            if not success:
                return False
            time.sleep(1)
        n = n - matches_requested
        last_match_id = matches[-1]['match_id']
    db.close()
    pass
