import pytest

@pytest.fixture
def lambda_input():
    return {
        'resource': '/',
        'path': '/',
        'httpMethod': 'POST',
        'headers': {
            'content-type': 'application/json; charset=utf-8',
            'Host': 'tgs5guku48.execute-api.ap-northeast-1.amazonaws.com',
            'User-Agent': 'LineBotWebhook/2.0',
            'X-Amzn-Trace-Id': 'Root=1-65e29e7c-616c5dbe4186ccc62dce914c',
            'X-Forwarded-For': '147.92.150.196',
            'X-Forwarded-Port': '443',
            'X-Forwarded-Proto': 'https',
            'x-line-signature': 'u3SqF1+bMuV+O5OZYRaVi1/3tiZ6EMMbZ9zNbmb9BuY='},
        'multiValueHeaders': {
            'content-type': ['application/json; charset=utf-8'],
            'Host': ['tgs5guku48.execute-api.ap-northeast-1.amazonaws.com'],
            'User-Agent': ['LineBotWebhook/2.0'],
            'X-Amzn-Trace-Id': ['Root=1-65e29e7c-616c5dbe4186ccc62dce914c'],
            'X-Forwarded-For': ['147.92.150.196'],
            'X-Forwarded-Port': ['443'],
            'X-Forwarded-Proto': ['https'],
            'x-line-signature': ['u3SqF1+bMuV+O5OZYRaVi1/3tiZ6EMMbZ9zNbmb9BuY=']},
        'queryStringParameters': None,
        'multiValueQueryStringParameters': None, 
        'pathParameters': None, 
        'stageVariables': None, 
        'requestContext': {
            'resourceId': 'e6oh9vjeo2', 
            'resourcePath': '/', 
            'httpMethod': 'POST', 
            'extendedRequestId': 
            'T-2zcEtyNjMEKpg=', 
            'requestTime': '02/Mar/2024:03:35:24 +0000', 
            'path': '/prod/', 
            'accountId': '225245440232', 
            'protocol': 'HTTP/1.1', 
            'stage': 'prod', 
            'domainPrefix': 
            'tgs5guku48', 
            'requestTimeEpoch': 1709350524176, 
            'requestId': '4841dc35-5a4c-4afb-adbf-4f95b5f3c32f', 
            'identity': {
                'cognitoIdentityPoolId': None, 
                'accountId': None, 
                'cognitoIdentityId': None, 
                'caller': None, 
                'sourceIp': '147.92.150.196', 
                'principalOrgId': None, 
                'accessKey': None,
                'cognitoAuthenticationType': None,
                'cognitoAuthenticationProvider': None, 
                'userArn': None, 
                'userAgent': 'LineBotWebhook/2.0', 
                'user': None}, 
            'domainName': 'tgs5guku48.execute-api.ap-northeast-1.amazonaws.com', 
            'deploymentId': 'sviajs', 
            'apiId': 'tgs5guku48'}, 
        'body': \
        """
        {"destination":"U61b2090558cde027a2081cef4fd5fcc1",
        "events":[{
            "type":"message",
            "message":{
                "type":"text",
                "id":"497476699521548625",
                "quoteToken":"Y0AnOYi_53bsx7JTG8J-dtWHtvz0ej_hsfK4szbZaIVtTF7al_GWEEybum75TwqAbB7ASM6dt7JYKb64gkRKPAjUwWwFt_-wGY8Zn9yTT695rXVtNU5Iq1lTvTAtSNd6_36oeIYi7s63QUW0yFzjcQ",
                "text":"嗨"},
            "webhookEventId":"01HQYKP56F4NJGQKTZMZVCGB44",
            "deliveryContext":{"isRedelivery":false},
            "timestamp":1709350523603,
            "source":{"type":"user","userId":"Ue098b5c4904665ed18454654c9d6c218"},
            "replyToken":"d6af095ca7dd4605840768bde1ff5aab","mode":"active"}]}""", 
            'isBase64Encoded': False
        }


@pytest.fixture
def mock_env_aws_auth(monkeypatch):
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "mock_key_id")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "mock_secret")