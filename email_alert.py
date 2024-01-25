import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# SendGrid API key
sendgrid_api_key = 'your_sendgrid_api_key'

# Email details
sender_email = '***********@example.com'
recipient_email = '***********@example.com'
subject = 'New Object Identified'
message_content = 'Hi, Group of Elephants identified near Zone 1'

# Create SendGrid mail object
message = Mail(
    from_email=sender_email,
    to_emails=recipient_email,
    subject=subject,
    html_content=message_content
)

# Set up the SendGrid API client
sg = SendGridAPIClient(sendgrid_api_key)

# Send email
response = sg.send(message)

print(f"Email sent with status code: {response.status_code}")