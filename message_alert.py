from twilio.rest import Client

# Twilio credentials
account_sid = '#########'
auth_token = '######'
twilio_phone_number = '########'
recipient_phone_number = '########'

# Create a Twilio client
client = Client(account_sid, auth_token)

# Send SMS
message = client.messages.create(
    body='Object detected',
    from_=twilio_phone_number,
    to=recipient_phone_number
)

print(f"SMS sent with SID: {message.sid}")