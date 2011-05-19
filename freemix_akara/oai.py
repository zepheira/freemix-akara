# -*- encoding: utf-8 -*-
'''
@ 2011 by Uche ogbuji <uche@ogbuji.net>

This file is part of the open source Akara project,
provided under the Apache 2.0 license.
See the files LICENSE and NOTICE for details.
Project home, documentation, distributions: http://wiki.xml3k.org/Akara

 Module name:: freemix_akara.oai

Scrapes collections from a OAI site into JSON form for Freemix

= Defined REST entry points =

http://purl.org/com/zepheira/freemix/services/oai.json (freemix_akara.oai) Handles GET

= Configuration =

None

= Notes on security =

This makes heavy access to remote OAI sites

= Notes =

'''

import sys, time

from amara.thirdparty import json

from akara.services import simple_service
from akara import logger
from akara import module_config

from zen.oai import oaiservice

LISTSETS_SERVICE_ID = 'http://purl.org/com/zepheira/freemix/services/oai/listsets'

@simple_service('GET', LISTSETS_SERVICE_ID, 'oai.listsets.json', 'application/json')
def listsets(endpoint='http://dspace.mit.edu/oai/request', limit=100):
    """
    e.g.:

    curl "http://localhost:8880/oai.listsets.json?limit=10"
    """
    limit = int(limit)
    remote = oaiservice(endpoint, logger)
    sets = remote.list_sets()[:limit]
    return json.dumps(sets, indent=4)


LISTRECORDS_SERVICE_ID = 'http://purl.org/com/zepheira/freemix/services/oai/listrecords'

@simple_service('GET', LISTRECORDS_SERVICE_ID, 'oai.listrecords.json', 'application/json')
def listrecords(endpoint='http://dspace.mit.edu/oai/request', oaiset=None, limit=100):
    """
    e.g.:

    curl "http://localhost:8880/oai.listrecords.json?oaiset=hdl_1721.1_18193&limit=10"
    """
    limit = int(limit)
    if not oaiset:
        raise ValueError('OAI set required')

    remote = oaiservice(endpoint, logger)
    records = remote.list_records(oaiset)[:limit]
    exhibit_records = []
    for rid, rinfo in records:
        erecord = {u'id': rid}
        for k, v in rinfo.iteritems():
            if len(v) == 1:
                erecord[k] = v[0]
            else:
                erecord[k] = v
            if u'title' in erecord:
                erecord[u'label'] = erecord[u'title']
            exhibit_records.append(erecord)
            
    #FIXME: This profile is NOT correct.  Dumb copy from CDM endpoint.  Please fix up below
    return json.dumps({'items': exhibit_records, 'data_profile': PROFILE}, indent=4)


#FIXME: This profile is NOT correct.  Dumb copy from CDM endpoint.
PROFILE = {
    #"original_MIME_type": "application/vnd.ms-excel", 
    #"Akara_MIME_type_magic_guess": "application/vnd.ms-excel", 
    #"url": "/data/uche/amculturetest/data.json", 
    #"label": "amculturetest", 
    "properties": [
        {
            "property": "handle", 
            "enabled": True, 
            "label": "Handle", 
            "tags": [
                "property:type=text", "property:type=shredded_list"
            ]
        }, 
        {
            "property": "language", 
            "enabled": True, 
            "label": "Language", 
            "types": [
                "text"
            ], 
            "tags": [
            ]
        }, 
        {
            "property": "creator", 
            "enabled": True, 
            "label": "Creators", 
            "tags": [
                "property:type=text", "property:type=shredded_list"
            ]
        }, 
        {
            "property": "format", 
            "enabled": True, 
            "label": "Formats", 
            "tags": [
                "property:type=text", "property:type=shredded_list"
            ]
        }, 
        {
            "property": "relation", 
            "Enabled": True, 
            "label": "Relations", 
            "tags": [
                "property:type=text", "property:type=shredded_list"
            ]
        }, 
        {
            "property": "id", 
            "enabled": False, 
            "label": "id", 
            "types": [
                "text"
            ], 
            "tags": [
                "property:type=url"
            ]
        }, 
        {
            "property": "date", 
            "enabled": True, 
            "label": "Date", 
            "tags": [
                "property:type=datetime", "property:type=shredded_list"
            ]
        }, 
        {
            "property": "datestamp", 
            "enabled": True, 
            "label": "Date stamp", 
            "types": [
                "datetime"
            ], 
            "tags": []
        }, 
        {
            "property": "title", 
            "enabled": True, 
            "label": "Title", 
            "types": [
                "text"
            ], 
            "tags": []
        }, 
        {
            "property": "label", 
            "enabled": True, 
            "label": "Label", 
            "types": [
                "text"
            ], 
            "tags": []
        }, 
        {
            "property": "type", 
            "enabled": True, 
            "label": "Document Type", 
            "types": [
                "text"
            ], 
            "tags": []
        }, 
    ], 
    #"Akara_MIME_type_guess": "application/vnd.ms-excel"
}