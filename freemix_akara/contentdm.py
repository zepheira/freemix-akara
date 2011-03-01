'''
( http://www.contentdm.com/ )

python contentdm_adapter.py http://digital.library.louisville.edu/cdm4/ "crutches"

 * http://digital.library.louisville.edu/collections/jthom/
 * http://digital.library.louisville.edu/cdm4/search.php
'''

import sys, time
#import datetime

import amara
from amara import bindery
from amara import tree
from amara.thirdparty import json
from amara.bindery.html import parse as htmlparse
from amara.bindery.util import dispatcher, node_handler
from amara.lib.iri import absolutize
from amara.lib.util import first_item

from akara.services import simple_service
from akara import logger
from akara import module_config

from zen.geo import geolookup
from zen.contentdm import read_contentdm


DEFAULT_SITE = 'http://digital.library.louisville.edu/cdm4/'
SERVICE_ID = 'http://purl.org/com/zepheira/freemix/services/contentdm.json'

@simple_service('GET', SERVICE_ID, 'contentdm.json', 'application/json')
def contentdm(collection='all', query=None, site=DEFAULT_SITE, limit=None):
    '''
    Search all collections in Louisville:

    curl "http://localhost:8880/contentdm.json?query=crutches&site=http://digital.library.louisville.edu/cdm4/"

    Search just /jthom collection in Louisville:

    curl "http://localhost:8880/contentdm.json?collection=/jthom&query=crutches&site=http://digital.library.louisville.edu/cdm4/"

    Search all collections in U Miami:

    curl "http://localhost:8880/contentdm.json?collection=/jthom&query=crutches&site=http://doyle.lib.muohio.edu/cdm4/"

    curl "http://localhost:8880/contentdm.json?collection=/jthom&site=http://digital.library.louisville.edu/cdm4/&sink=http://localhost:8880/testsink.json"
    '''
    results = read_contentdm(site, collection=collection, query=query, limit=limit)
    header = results.next()
    url = header['basequeryurl']
    count = 0
    logger.debug("Start URL: " + repr(url))
    entries = list(results)
    return json.dumps({'items': entries}, indent=4)

