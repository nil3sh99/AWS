# Basic Code
# import json

# def lambda_handler(event, context):
#     # TODO implement
#     return {
#         'statusCode': 200,
#         'body': json.dumps('Hello from Lambda!')
#     }

# arn: arn:aws:lambda:ca-central-1:507638485545:function:MockAPIFunction

class TooManyRequestsException(Exception): pass
class ServerUnavailableException(Exception): pass
class UnknownException(Exception): pass

def lambda_handler(event, context):
    statuscode = event["statuscode"]    
    if statuscode == "429":
        raise TooManyRequestsException('429 Too Many Requests')
    elif statuscode == "503":
        raise ServerUnavailableException('503 Server Unavailable')
    elif statuscode == "200":
        return '200 OK'
    else:
        raise UnknownException('Unknown error')

