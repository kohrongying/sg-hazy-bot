import json


def lambda_handler(event, context):
    body = {
        "message": "Test123456",
    }
    print(event)
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
