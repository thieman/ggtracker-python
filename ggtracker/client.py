#!/usr/bin/env python

""" GGTracker client classes, for trackin' yo' GGs

I mean, obviously they're not my GGs, I only win games. """

import time
import urlparse

import requests

__author__       = 'Travis Thieman'
__credits__      = ['David Joerg']
__license__      = 'BSD'
__code_quality__ = 'Pretty poor, honestly'


class GGTrackerAPI(object):
    """ Factory for creating queries against the API """

    def __init__(self, url, rate_limit=60, api_version=1):
        """ Instantiate a new client for querying.

        This instance maintains instance-level compliance with
        requirements such as courtesy rate limits.

        url: GGtracker API URI. scheme defaults to http if not provided.
        rate_limit: requests allowed per minute, default 60. 0 to disable.
        api_version: specify the version of the GGTracker API to target
        """

        self.known_endpoints = ['identities', 'matches']

        self.rate_limit = rate_limit
        self.api_version = api_version

        parsed_uri = urlparse.urlparse(url)
        if not parsed_uri.scheme:
            parsed_uri = urlparse.urlparse('http://' + url)

        self.base_url = parsed_uri.netloc
        self.scheme = parsed_uri.scheme

        components =  [self.base_url, 'api', ''.join(['v', str(self.api_version)])]
        self.target = '/'.join([s.strip('/') for s in components])
        self.target = '://'.join([self.scheme, self.target])

        self.request_log = []


    def __repr__(self):
        return '<GGTrackerAPI (url: %s, limit: %d, v: %d)>' % (self.target,
                                                               self.rate_limit,
                                                               self.api_version)


    def query(self, endpoint):
        if endpoint not in self.known_endpoints:
            raise ValueError('unknown endpoint')
        block_time = self._get_block_time_seconds()
        self._insert_request_to_log(block_time)
        return GGTrackerQuery('/'.join([self.target, endpoint]),
                              endpoint, block_time)


    def _get_block_time_seconds(self):
        """ Returns float of the number of seconds to wait before
        the request limit will no longer be exceeded. Also clears out
        any requests older than a minute.

        This makes an important asssumption that your program will actually
        honor the block time. If you don't, you will rocket past the courtesy
        rate limit. This is also the most thread-unsafe thing ever. """

        if self.rate_limit == 0:
            return 0

        call_time = time.time()
        remove_time = call_time - 60

        for idx, request in enumerate(self.request_log):
            if request >= remove_time:
                self.request_log = self.request_log[idx:]
                break

        if len(self.request_log) < self.rate_limit:
            return 0
        return (self.request_log[-1 * self.rate_limit] + 60) - call_time


    def _insert_request_to_log(self, block_time=0):
        """ Inserts a new timestamp into the request log, marked block_time
        seconds in the future. """
        if self.rate_limit == 0:
            return
        self.request_log.append(time.time() + block_time)


class GGTrackerQuery(object):
    """ Constructs a query against the API and executes as a GET request.

    Query constructor methods are chainable. Requests are only executed
    upon a few explicit commands.

    The query will block *on creation* if the rate limit is exceeded from
    the parent API object. If you don't like this, disable the rate limit.
    """

    def __init__(self, uri, endpoint, block_time=0):
        """ Create a new query against the specified URI.

        The preferred method of modifying the query parameters is through
        chainable methods. """

        if block_time:
            time.sleep(block_time)

        self.uri = uri
        self.endpoint = endpoint
        self._limit = 10
        self._offset = 0
        self._paginate = False
        self._order = None
        self._filters = {}
        self._match = {}
        self.result = None


    def __repr__(self):
        return '<GGTrackerQuery (uri: %s)>' % self.uri


    def __iter__(self):
        """ Iterate over the result set """
        self._get()
        for rec in self.result.get('collection', []):
            yield rec


    def _get(self):
        """ Execute the stored query """

        if self.result is None:
            payload = self._construct_payload()
            r = requests.get(self.uri, params=payload)
            r.raise_for_status()
            self.result = r.json()


    def one(self):
        """ Returns the first (and only) doc in the result set, otherwise
        raises an exception. """

        self._get()
        if len(self.result.get('collection', [])) != 1:
            raise ValueError('query did not return exactly one result')
        return self.result['collection'][0]


    def _construct_payload(self):

        payload = {}

        for attr in ['_limit', '_offset', '_order']:
            if getattr(self, attr) is not None:
                payload[attr.lstrip('_')] = getattr(self, attr)

        if self._paginate:
            payload['paginate'] = 'true'

        for k, v in self._match.iteritems():
            payload[k] = v

        # special case for clearing all filters
        if self._filters.get('clear', False) == True:
            payload['filter'] = ''

        else:
            filter_parts = []
            for k, v in self._filters.iteritems():

                if not v:  # filter without list args, like "-graphs"
                    filter_parts.append('-' + k)
                else:
                    filter_list = []
                    for element in v:
                        filter_list.append('-' + element)
                    filter_parts.append(''.join([k, '(', ','.join(filter_list), ')']))

            if filter_parts:
                payload['filter'] = ','.join(filter_parts)

        return payload


    def limit(self, limit):
        self._limit = limit
        return self


    def offset(self, offset):
        self._offset = offset
        return self


    def paginate(self, enable=True):
        self._paginate = enable
        return self


    def order(self, order):
        self._order = order
        return self


    def stats(self, stats):
        # TODO: figure out how these actually work
        raise NotImplementedError()


    def match(self, **kwargs):
        """ Add one or many new matching filters to the filter
        set using kwargs.

        These aren't what go in the actual 'filter' URL parameter. These
        are used to match against the db, like name=Zoulas """

        for filter_name, filter_value in kwargs.iteritems():
            self._match[filter_name] = filter_value
        return self


    def filter(self, **kwargs):
        """ Add one or many new matching filters to the filter
        set using kwargs. """

        for filter_name, filter_value in kwargs.iteritems():
            self._filters[filter_name] = filter_value
        return self
