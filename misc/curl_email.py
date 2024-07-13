# Define the curl command as a list of strings
curl_command = [
    'curl',
    '--ssl-reqd',
    '--url', 'smtp://sandbox.smtp.mailtrap.io:2525',
    '--user', '36186b4d6ce82a:6531c67149aa2a',
    '--mail-from', 'from@example.com',
    '--mail-rcpt', 'to@example.com',
    '--upload-file', '-'
]

# Define the email content to be passed to curl
email_content = """
From: osi@osinachi.me
To: ralph@osinachi.me
Subject: You are awesome!


This is supposed to work

"""

