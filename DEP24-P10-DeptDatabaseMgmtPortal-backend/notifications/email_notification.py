from .models import userNotifications,broadcastNotifications
from django.core.mail import EmailMessage,send_mail,EmailMultiAlternatives
from usercustom.models import CustomUser

def email_notification(mailing_list,subject,message,user,create = False):
    if(create):
        obj = userNotifications.objects.create(user = user,notification = subject,message = message)
        obj.save()
    mailing_list.append(user)
    mailing_lis = []
    for user in mailing_list:
        if user.get_email_notification:
            mailing_lis.append(user.email)
    try:
        msg = EmailMessage(subject, message,'donotreplydepartmentdata@gmail.com',mailing_lis)
        msg.content_subtype = "html"
        msg.send(fail_silently=False)
    except  Exception as e:
        print(e)



def email_broadcast_notification(request, subject,message,group, create = False):
    if create:
        bn = broadcastNotifications.objects.create(group = group,notification = subject,message = message)
        bn.save()
    users = None
    print('group:',group)
    if group == None:
        print('a')
        users = CustomUser.objects.all().filter(department = request.user.department)
        print(users)
    else:
        print('b')
        users = group.user_set.all().filter(department = request.user.department)
    emails = [user.email for user in users if user.get_email_broadcast_notification]
    print(emails)
    try:
        msg = EmailMessage(subject, message,'donotreplydepartmentdata@gmail.com',['donotreplydepartmentdata@gmail.com'],bcc =  emails)
        msg.content_subtype = "html"
        msg.send(fail_silently=False)
    except Exception as e:
        print(e)


