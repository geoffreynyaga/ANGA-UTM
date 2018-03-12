


from fcm_django.models import FCMDevice

def send_not():

    device = FCMDevice.objects.all().first()
    print(device)

    device.send_message("Title", "Message")
    device.send_message(data={"test": "test"})
    device.send_message(title="Title", body="Message", icon=..., data={"test": "test"})
