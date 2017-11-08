from twilio.rest import Client

account_sid = 'AC84ad76552c7d3a00d6c3fbf9998d1dd2'
auth_token = 'TOKEN'

client = Client(account_sid, auth_token)

BASE_URL = 'https://api.twilio.com/2010-04-01/Accounts/AC84ad76552c7d3a00d6c3fbf9998d1dd2/Messages.json'

def notice(message, phone_number):
    message = client.messages.create(
        to='+1%s' % phone_number,
        from_='+13437005464',
        body = message)
