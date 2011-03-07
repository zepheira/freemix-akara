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
    return json.dumps({'items': entries, 'data_profile': PROFILE}, indent=4)

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
            "types": [
                "text"
            ], 
            "tags": [
                "property:type=list"
            ]
        }, 
        {
            "property": "Locations_Depicted", 
            "enabled": True, 
            "label": "Depicted locations", 
            "types": [
                "text"
            ], 
            "tags": [
                "property:type=list"
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
