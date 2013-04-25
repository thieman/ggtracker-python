ggtracker-python
================

A simple API client for [GGTracker.](http://ggtracker.com)

## Installation

    pip install ggtracker-client

## Usage

First, get yourself a client.

    from ggtracker import GGTrackerAPI
    gg = GGTrackerAPI('api.ggtracker.com')

You can construct queries by supplying an endpoint and chaining together the following modifiers.

  * limit(int)
  * offset(int)
  * paginate()
  * order(int)
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
