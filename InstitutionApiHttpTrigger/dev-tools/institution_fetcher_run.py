"""

This module can be used during dev and debug for
testing the institution fetcher without the need
to invoke it via the Azure function.
"""


import inspect
import json
import logging
import os
import sys

logging.basicConfig(level=logging.DEBUG)


CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PARENTDIR = os.path.dirname(CURRENTDIR)
GRANDPARENTDIR = os.path.dirname(PARENTDIR)
GREATGRANDPARENTDIR = os.path.dirname(GRANDPARENTDIR)
sys.path.insert(0, PARENTDIR)
sys.path.insert(0, GRANDPARENTDIR)
sys.path.insert(0, GREATGRANDPARENTDIR)

from institution_fetcher import InstitutionFetcher

from SharedCode import utils


def test_institution_fetcher():
    db_id = "AzureCosmosDbDatabaseId"
    collection_id = "AzureCosmosDbInstitutionsCollectionId"

    # Get the relevant properties from Application Settings
    collection_link = utils.get_collection_link(db_id, collection_id)

    client = utils.get_cosmos_client()
    institution_fetcher = InstitutionFetcher(client, collection_link)
    institution_id = "10007857"
    version = 1
    return institution_fetcher.get_institution(institution_id, version)


institution_json = test_institution_fetcher()
institution_json_dict = json.loads(institution_json)
print(json.dumps(institution_json_dict, indent=4))
