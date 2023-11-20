import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def inform_user_about_updates(receiver,subject,body):
    # Replace these with your Gmail account details and email content
    gmail_user = 'amit@sutara.org'
    gmail_app_password = 'pjwt jlkx weuj dzwg'
     # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = ', '.join(receiver)
    msg['Subject'] = subject

    # Add the body of the email
    msg.attach(MIMEText(body, 'plain'))
    # Generate the report
    # report_content = f"Missing audios in google drive-->\n{body}"
     
    

    try:
        # msg.attach(MIMEText(report_content, 'plain'))
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_app_password)
        server.sendmail(gmail_user, receiver, msg.as_string())
        server.close()
        
        print('Email sent!')
    except Exception as exception:
        inform_user_about_updates(receiver,"Error in Building Lamguage",e)
        print("Error: %s!\n\n" % exception)