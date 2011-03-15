'''
Requires the Zen library.

( http://www.contentdm.com/ )

python contentdm_adapter.py http://digital.library.louisville.edu/cdm4/ "crutches"

 * http://digital.library.louisville.edu/collections/jthom/
 * http://digital.library.louisville.edu/cdm4/search.php
'''

import sys, time

from amara.thirdparty import json

from akara.services import simple_service
from akara import logger
from akara import module_config

from zen.oai import oaiservice

SERVICE_ID = 'http://purl.org/com/zepheira/freemix/services/oai/listsets'

@simple_service('GET', SERVICE_ID, 'oai.listsets.json', 'application/json')
def oai(endpoint='http://dspace.mit.edu/oai/request', limit=100):
    """
    """
    limit = int(limit)
    remote = oaiservice(endpoint, logger)
    sets = remote.list_sets()[:limit]
    #logger.debug("Start URL: " + repr(url))
    #logger.debug("Limit: {0}".format(limit))
    return json.dumps(sets, indent=4)


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
