'''
Requires the Zen library.
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
            "property": "Object_Type", 
            "enabled": True, 
            "label": "Object type", 
            "types": [
                "text"
            ], 
            "tags": []
        }, 
        {
            "property": "Source", 
            "enabled": True, 
            "label": "Source", 
            "types": [
                "text"
            ], 
            "tags": [
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
            "property": "link", 
            "enabled": True, 
            "label": "link", 
            "types": [
                "text"
            ], 
            "tags": [
                "property:type=url"
            ]
        }, 
        {
            "property": "Collection", 
            "enabled": True, 
            "label": "Collection", 
            "types": [
                "text"
            ], 
            "tags": [
            ]
        }, 
        {
            "property": "Digital_Publisher", 
            "enabled": True, 
            "label": "Digital publisher", 
            "types": [
                "text"
            ], 
            "tags": []
        }, 
        {
            "property": "Description", 
            "enabled": True, 
            "label": "Description", 
            "types": [
                "text"
            ], 
            "tags": []
        }, 
        {
            "property": "label", 
            "enabled": False, 
            "label": "label", 
            "types": [
                "text"
            ], 
            "tags": []
        }, 
        {
            "property": "Format", 
            "enabled": True, 
            "label": "Format", 
            "types": [
                "text"
            ], 
            "tags": []
        }, 
        {
            "property": "Estimated_Original_Date", 
            "enabled": True, 
            "label": "Estimated original date", 
            "types": [
                "text"
            ], 
            "tags": []
        }, 
        {
            "property": "Date_Original", 
            "enabled": True, 
            "label": "Original date", 
            "types": [
                "text"
            ], 
            "tags": []
        }, 
        {
            "property": "thumbnail", 
            "enabled": True, 
            "label": "thumbnail", 
            "types": [
                "text"
            ], 
            "tags": [
                "property:type=image"
            ]
        }, 
        {
            "property": "imageuri", 
            "enabled": True, 
            "label": "imageuri", 
            "types": [
                "text"
            ], 
            "tags": [
                "property:type=image"
            ]
        }, 
        {
            "property": "tags", 
            "enabled": True, 
            "label": "tags",
            "tags": [
                "property:type=text", "property:type=shredded_list"
            ]
        },
        {
            "property": "Locations_Depicted", 
            "enabled": True, 
            "label": "Depicted locations", 
            "tags": [
                "property:type=text", "property:type=shredded_list"
            ]
        }, 
        {
            "property": "Creator", 
            "enabled": True, 
            "label": "Creator", 
            "types": [
                "text"
            ], 
            "tags": []
        }, 
        {
            "property": "Image_Number", 
            "enabled": True, 
            "label": "Image number", 
            "types": [
                "text"
            ], 
            "tags": []
        }, 
        {
            "property": "Collection_Website", 
            "enabled": True, 
            "label": "Collection website", 
            "types": [
                "text"
            ], 
            "tags": [
                "property:type=url"
            ]
        }, 
        {
            "property": "Citation_Information", 
            "enabled": True, 
            "label": "Citation information", 
            "types": [
                "text"
            ], 
            "tags": []
        }, 
    ], 
    #"Akara_MIME_type_guess": "application/vnd.ms-excel"
}
