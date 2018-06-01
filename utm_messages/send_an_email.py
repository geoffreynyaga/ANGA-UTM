from django.core.mail import send_mail

send_mail('Test SendGrid Message', 'There\'s always a first.', 'gn@geoffreynyaga.com',
                  ['web-d3dix@mail-tester.com'], fail_silently=False)

# send_mail(subject,body, from_email, [to_email], fail_silently=False)

