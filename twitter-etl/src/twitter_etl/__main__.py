import json
import logging
from unittest.mock import Mock

from twitter_etl.main import main

logging.basicConfig(level=logging.INFO)

REQUEST_PAYLOAD = '''{}'''
request = Mock()
request.get_json.return_value = json.loads(REQUEST_PAYLOAD)
request.get_data.return_value = REQUEST_PAYLOAD.encode()
request.method = 'POST'

main(request)