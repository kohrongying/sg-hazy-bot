import json
from api_service import main

def lambda_handler(event, context):
    update = json.loads(event['body'])

    body = {
        'method': 'sendMessage',
        'chat_id': update['message']['chat']['id'],
        'parse_mode': 'Markdown',
        'text': main(),
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
