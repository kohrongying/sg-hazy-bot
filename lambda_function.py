import json
import base 64
from api_service import main


def lambda_handler(event, context):
    decoded_body = base64.b64decode(event['body'])
    print(decoded_body)
    update = json.loads(decoded_body)
    
    body = {
        'method': 'sendMessage',
        'chat_id': update['message']['chat']['id'],
        'parse_mode': 'HTML',
        'text': main(),
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
