import sendgrid

from sendgrid.helpers.mail import *

import secrets
from supports.database import transaction_to_email as tte

sg = sendgrid.SendGridAPIClient(apikey='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')

def send(content_in, to_email_in):
    from_email = Email('jasonle@cmail.carleton.ca')
    to_email = Email(to_email_in)
    subject = 'Notice from '
    content = Content("text/plain", content_in)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())

def report(transaction):
    content = "The transaction of %s looks funny" % (str(transaction),)
    send(content, tte(transaction))
