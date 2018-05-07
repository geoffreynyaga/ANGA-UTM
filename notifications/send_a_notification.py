from webpush import send_user_notification


"""" the head and body parameters must be a string
In user parameter, a user object should be passed
The user will get notification to all of his subscribed browser. A user can subscribe many browsers.
"""
def send_a_notification(user,head,body):

    payload = {"head": head, "body": body}

    send_user_notification(user=user, payload=payload, ttl=1000)
