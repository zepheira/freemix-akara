'''
( http://www.contentdm.com/ )

python contentdm_adapter.py http://digital.library.louisville.edu/cdm4/ "crutches"

 * http://digital.library.louisville.edu/collections/jthom/
 * http://digital.library.louisville.edu/cdm4/search.php
'''

import sys, time
import datetime
import urllib, urlparse, urllib2
from cgi import parse_qs
import cStringIO
import feedparser
from itertools import *

import simplejson
import httplib2

import amara
from amara import bindery
from amara import tree
from amara.writers.struct import *
from amara.bindery.html import parse as htmlparse
from amara.bindery.util import dispatcher, node_handler
from amara.lib.iri import absolutize
from amara.lib.util import first_item

from akara.services import simple_service
from akara import logger
from akara import module_config

from zenlib.geo import geolookup


DEFAULT_SITE = 'http://digital.library.louisville.edu/cdm4/'

#QUERY = sys.argv[2]
#URL = 'item_viewer.php?CISOROOT=/jthom&CISOPTR=920&CISOBOX=1&REC=1'


class content_handlers(dispatcher):
    @node_handler([u'br'])
    def br(self, node):
        yield u', '

    @node_handler(u'span')
    def code(self, node):
        for chunk in chain(*imap(self.dispatch, node.xml_children)):
            yield chunk

    #@node_handler([u'text()'])
    #def text(self, node):
    #    yield node.xml_value

    @node_handler([u'*'], priority=-1)
    def default(self, node):
        yield unicode(node)

CONTENT = content_handlers()

SERVICE_ID = 'http://purl.org/com/zepheira/freemix/services/contentdm.json'

@simple_service('GET', SERVICE_ID, 'contentdm.json', 'application/json')
def contentdm(collection='all', query=None, site=DEFAULT_SITE, sink=None):
    '''
    Search all collections in Louisville:

    curl "http://localhost:8880/contentdm.json?query=crutches&site=http://digital.library.louisville.edu/cdm4/"

    Search just /jthom collection in Louisville:

    curl "http://localhost:8880/contentdm.json?collection=/jthom&query=crutches&site=http://digital.library.louisville.edu/cdm4/"

    Search all collections in U Miami:

    curl "http://localhost:8880/contentdm.json?collection=/jthom&query=crutches&site=http://doyle.lib.muohio.edu/cdm4/"

    curl "http://localhost:8880/contentdm.json?collection=/jthom&site=http://digital.library.louisville.edu/cdm4/&sink=http://localhost:8880/testsink.json"
    '''
    qstr = urllib.urlencode({'CISOBOX1' : query or '', 'CISOROOT' : collection})
    url = '%sresults.php?CISOOP1=any&%s&CISOFIELD1=CISOSEARCHALL'%(site, qstr)
    logger.debug("initial URL: " + url)
    resultsdoc = htmlparse(url)

    entries = []
    seen = set()

    #items = resultsdoc.xml_select(u'//form[@name="searchResultsForm"]//a[starts-with(@href, "item_viewer.php")]')

    if sink:
        #Only follow pagination if a sink is given to push back
        def follow_pagination(doc):
            #e.g. of page 1: http://digital.library.louisville.edu/cdm4/browse.php?CISOROOT=/afamoh
            #e.g. of page 2: http://digital.library.louisville.edu/cdm4/browse.php?CISOROOT=/afamoh&CISOSTART=1,21
            page_start = 1
            while True:
                items = doc.xml_select(u'//a[starts-with(@href, "item_viewer.php")]')
                for i in items: yield i
                next = [ l.href for l in doc.xml_select(u'//a[@class="res_submenu"]') if int(l.href.split(u',')[-1]) > page_start ]
                #logger.debug("NEXT: " + repr(next))
                if not next:
                    break
                page_start = int(l.href.split(u',')[-1])
                url = absolutize(next[0], site)
                logger.debug("Next page URL: " + url)
                doc = htmlparse(url)
            return
        items = follow_pagination(resultsdoc)
    else:
        items = resultsdoc.xml_select(u'//a[starts-with(@href, "item_viewer.php")]')

    for it in items:
    #for it in islice(items, 0, 1):
        entry = {}
        pageuri = absolutize(it.href, site)
        logger.debug("Processing item URL: " + pageuri)
        (scheme, netloc, path, query, fragment) = urlparse.urlsplit(pageuri)
        params = parse_qs(query)
        entry['id'] = params['CISOPTR'][0]
        entry['label'] = entry['id']
        if entry['id'] in seen:
            continue
        seen.add(entry['id'])
        entry['link'] = unicode(pageuri)
        entry['local_link'] = '#' + entry['id']
        page = htmlparse(pageuri)
        image = first_item(page.xml_select(u'//td[@class="tdimage"]//img'))
        if image:
            imageuri = absolutize(image.src, site)
            entry['imageuri'] = imageuri
            try:
                entry['thumbnail'] = absolutize(dict(it.xml_parent.a.img.xml_attributes.items())[None, u'src'], site)
            except AttributeError:
                logger.debug("No thumbnail")
        #entry['thumbnail'] = DEFAULT_RESOLVER.normalize(it.xml_parent.a.img.src, root)
        fields = page.xml_select(u'//tr[td[@class="tdtext"]]')
        for f in fields:
            key = unicode(f.td[0].span.b).replace(' ', '_')
            value = u''.join(CONTENT.dispatch(f.td[1].span))
            entry[key] = unicode(value)
        if u"Location_Depicted" in entry:
            locations = entry[u"Location_Depicted"].split(u', ')
            locations = [ l.replace(' (', ', ').replace(')', '').replace(' ', '+') for l in locations if l.strip() ]
            logger.debug("LOCATIONS: " + repr(locations))
            #FIXME: Compute latlongs on Zen read, not write
            latlongs = []
            #for place in locations:
                latlong = geolookup(place)
                if latlong:
                    latlongs.append(latlong)
                #entry[u"Location_Depicted_latlong"] = location
            logger.debug("LOCATIONS: " + repr(latlongs))
            entry[u"Locations_Depicted_list"] = location
        if u"Date_Original" in entry:
            entry[u"Estimated_Original_Date"] = entry[u"Date_Original"].strip().replace('-', '5').replace('?', '')
        if u"Subject" in entry:
            entry[u"Subject"] = [ s for s in entry[u"Subject"].split(', ') if s.strip() ]
        entries.append(entry)

    return simplejson.dumps({'items': entries}, indent=4)

