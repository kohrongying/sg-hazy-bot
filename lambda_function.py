import json
import base64
from aqicn import format_aqicn_response
from nea import format_nea_response


def lambda_handler(event, context):
    decoded_body = base64.b64decode(event['body'])
    update = json.loads(decoded_body)
    
    user_message = update['message']['text'].strip().lower()
    
    if 'aqicn' in user_message:
        print(f'User requested AQICN data: {user_message}')
        response_text = format_aqicn_response()
    else:
        print(f'User requested NEA data: {user_message}')
        response_text = format_nea_response()

    body = {
        'method': 'sendMessage',
        'chat_id': update['message']['chat']['id'],
        'parse_mode': 'HTML',
        'text': response_text,
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
