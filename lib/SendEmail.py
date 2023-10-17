import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class SendEmail():

    sender_email = 'secgizmobox@gmail.com'
    sender_password = 'eevl vyqp heju suol'

    def sending(self, receiver_email, subject, body, attachment_path):
        name = str(attachment_path.split('/')[-1])
        # Create a multipart message
        message = MIMEMultipart()
        message['sender_email'] = self.sender_email
        message['receiver_email'] = receiver_email
        message['subject'] = subject
    
        # Add body to email
        message.attach(MIMEText(body, 'plain'))

        # Open the file in bynary
        with open(attachment_path, 'rb') as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEApplication(attachment.read(), Name=name)
            part['Content-Disposition'] = f'attachment; filename="{name}"'
            message.attach(part)

        # Log in to server using secure context and send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, receiver_email, message.as_string())
            server.quit()