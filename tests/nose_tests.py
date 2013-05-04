from ggtracker import GGTrackerAPI, GGTrackerQuery

gg = None


def setup():
    global gg
    gg = GGTrackerAPI('api.ggtracker.com',
                      rate_limit=0,
                      api_version=1)


def test_alternate_constructor_uris():
    GGTrackerAPI('http://api.ggtracker.com')


def test_default_identity_endpoint_valid():
    query = gg.query('identities')
    assert query.uri == 'http://api.ggtracker.com/api/v1/identities'


def test_default_match_endpoint_valid():
    query = gg.query('matches')
    print query.uri
    assert query.uri == 'http://api.ggtracker.com/api/v1/matches'


def test_empty_query_payload():
    query = gg.query('identities')
    assert query._construct_payload() == {'limit': 10, 'offset': 0}


def test_query_limit_setting():
    query = gg.query('identities').limit(20)
    assert query._construct_payload() == {'limit': 20, 'offset': 0}


def test_query_offset_setting():
    query = gg.query('identities').offset(10)
    assert query._construct_payload() == {'limit': 10, 'offset': 10}


def test_query_paginate_setting():
    query = gg.query('identities').paginate()
    assert query._construct_payload() == {'limit': 10, 'offset': 0,
                                          'paginate': 'true'}


def test_query_order_setting_ascending():
    query = gg.query('identities').order('played_at', ascending=True)
    assert query._construct_payload() == {'limit': 10, 'offset': 0,
                                          'order': '-played_at'}


def test_query_order_setting_descending():
    query = gg.query('identities').order('played_at', ascending=False)
    assert query._construct_payload() == {'limit': 10, 'offset': 0,
                                          'order': '_played_at'}


def test_query_sc2ranks_setting():
    query = gg.query('identities').sc2ranks()
    assert query._construct_payload() == {'limit': 10, 'offset': 0,
                                          'sc2ranks': 'true'}


def test_query_game_type_setting():
    query = gg.query('matches').game_type('1v1')
    assert query._construct_payload() == {'limit': 10, 'offset': 0,
                                          'game_type': '1v1'}


def test_query_game_type_invalid():
    try:
        query = gg.query('matches').game_type('8v8')
    except ValueError:
        return
    raise ValueError('test failed')


def test_query_match_setting():
    query = gg.query('identities').match(user='Zoulas').match(gateway='us')
    assert query._construct_payload() == {'limit': 10, 'offset': 0,
                                          'user': 'Zoulas', 'gateway': 'us'}


def test_query_filter_setting():
    query = gg.query('identities').filter(graphs=None).\
        filter(match=['replays', 'map']).\
        filter(entity=[])
    check_filter = '-graphs,match(-replays,-map),-entity'
    assert query._construct_payload() == {'limit': 10, 'offset': 0,
                                          'filter': check_filter}


def test_null_filter_setting():
    query = gg.query('matches').filter(clear=True)
    assert query._construct_payload() == {'limit': 10, 'offset': 0,
                                          'filter': ''}


def test_query_summary_setting():
    query = gg.query('matches').summary()
    assert query._construct_payload() == {'limit': 10, 'offset': 0,
                                          'summary': 'true'}


def test_rate_limit_blocking():
    fresh_client = GGTrackerAPI('api.ggtracker.com', rate_limit=60)
    for i in range(60):
        query = fresh_client.query('identities')
    assert fresh_client._get_block_time_seconds() > 0


def test_identities_returns_result():
    query = gg.query('identities')
    for rec in query:
        return
    assert False


def test_matches_returns_result():
    query = gg.query('matches')
    for rec in query:
        return
    assert False


def test_identity_one():
    query = gg.query('identities').match(user='Omni').\
        match(gateway='us').\
        match(bnet_id='273698')
    query.one()
