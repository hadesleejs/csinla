# -*- coding: UTF-8 -*-
#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "csinla.settings")
    import django
    django.setup()
    import csv
    from csinla_curricular.models import Curricular
    curricular_list=[]
    is_first=True
    csvfile = file('curricular.csv', 'rb')
    reader = csv.reader(csvfile)
    for row in reader:
        if is_first:
            is_first = False
        else:
            print row
            cds={
                'year':int(row[0] if row[0] else 0),
                'semester':row[1],
                'department':row[2],
                'subject':'%s %s' % (row[3],row[4]),
                'instructor':row[5],
                'sign_a':int(row[6] if row[6] else 0),
                'sign_b':int(row[7] if row[7] else 0),
                'sign_c':int(row[8] if row[8] else 0),
                'sign_d':int(row[9] if row[9] else 0),
                'sign_f':int(row[10] if row[10] else 0),
                'sign_ip':int(row[11] if row[11] else 0),
                'sign_ix':int(row[12] if row[12] else 0),
                'sign_np':int(row[13] if row[13] else 0),
                'sign_p':int(row[14] if row[14] else 0),
                'sign_w':int(row[15] if row[15] else 0),
                'sign_rd':int(row[16] if row[16] else 0),
                'sign_total':int(row[17] if row[17] else 0)
            }
            curricular=Curricular(**cds)
            curricular_list.append(curricular)
    if curricular_list:
        Curricular.objects.bulk_create(curricular_list)



