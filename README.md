ggtracker-python
================

A simple API client for [GGTracker.](http://ggtracker.com)

## Installation

Tagged versions are available on PyPi (though the 0.1 release is not tagged; my bad).

    pip install ggtracker-client

Otherwise, clone this repo for the latest and greatest.

## Usage

First, get yourself a client.

    from ggtracker import GGTrackerAPI
    gg = GGTrackerAPI('api.ggtracker.com')

You can construct queries by supplying an endpoint and chaining together the following modifiers. Explanations of the less-obvious methods can be found in their docstrings.

  * limit(int)
  * offset(int)
  * paginate()
  * summary()
  * sc2ranks()
  * game_type(str in ['1v1', '2v2', '3v3', '4v4', 'FFA'])
  * order(field_name, ascending=True)
  * match(user='Zoulas', gateway='us')
  * filter(graphs=None, match=['replays', 'map'])

Once you construct the query, you can then iterate over it, where each element is a member of the 'collection' list in the resulting JSON.

    query = gg.query('identities').limit(20).match(gateway='us').paginate()
    for record in query:
        do_stuff(record)

## Implementation Details

#### Rate Limit

The client supports a courtesy rate limit, defaulted to 60 requests per minute. If you exceed the rate limit, the client will block upon **creation** of a new query until enough time has passed. Rate limits can be altered by passing the number of permissible requests per minute to the constructor, or 0 to disable.

    gg = GGTrackerAPI('api.ggtracker.com', rate_limit=0)

#### Default Filters

If you do not explicitly set any filters, some API endpoints will assign default filters to your query in order to reduce load on GGTracker's API. This is intended behavior. If you would like to force no filters on your query, do the following:

    gg.query('matches').filter(clear=True)

## TODO

  * stats filters on the query are entirely unsupported right now
  * implement additional helper functions for common data manipulations
  * put some validation to catch invalid filters being applied

## Author

 * [Travis Thieman](https://twitter.com/thieman)

## Credits

 * [David Joerg](https://twitter.com/dsjoerg) for creating GGTracker and for helping me grok the API
