

from utm_messages.models import UserToUserMessages

def send_message(recepient, title, text):
    message = UserToUserMessages
    message.title = title
    message.text = text
    message.sender = request.user
    message.receiver = receiver
    message.save()
