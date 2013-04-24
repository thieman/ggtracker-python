from ggtracker import GGTrackerAPI, GGTrackerQuery, GGTrackerResult

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


def test_query_order_setting():
    query = gg.query('identities').order('_played_at')
    assert query._construct_payload() == {'limit': 10, 'offset': 0,
                                          'order': '_played_at'}


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


def test_rate_limit_blocking():
    fresh_client = GGTrackerAPI('api.ggtracker.com', rate_limit=60)
    for i in range(60):
        query = fresh_client.query('identities')
    assert fresh_client._get_block_time_seconds() > 0


def test_identities_returns_result():
    query = gg.query('identities')
    result = query.get()
    assert isinstance(result, GGTrackerResult)


def test_matches_returns_result():
    query = gg.query('matches')
    result = query.get()
    assert isinstance(result, GGTrackerResult)


def test_identity_one():
    query = gg.query('identities').match(user='Omni').\
        match(gateway='us').\
        match(bnet_id='273698')
    result = query.get()
    result.one()
