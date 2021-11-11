from django.core.mail import send_mail

def send_email():

    send_mail(
        subject='test',
        message='test',
        from_email='spodaily.app@gmail.com',
        recipient_list=['ugodimini@gmail.com']
              )
