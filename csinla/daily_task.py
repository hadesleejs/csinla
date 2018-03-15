# -*- coding: UTF-8 -*-
#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "csinla.settings")
    import django
    django.setup()
    import csv
    import datetime
    from csinla_accounts.models import Profile
    from utils.email_send import send_user_remove_mail
    for user in Profile.objects.filter(is_active=False,date_joined__lte=datetime.datetime.now()-datetime.timedelta(days=7)):
        send_user_remove_mail(user.email)
        user.delete()



