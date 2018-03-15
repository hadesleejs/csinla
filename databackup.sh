#!/bin/bash

mysqldump -uroot -pAdmin12345 csinla | gzip > /var/backups/csinla/db/csinla_$(date +%Y%m%d_%H%M%S).sql.gz

tar zcvf /var/backups/csinla/media/media_`date +%Y%m%d_%H%M%S`.tar.gz /var/www/csinla/csinla/media/ 
tar zcvf /var/backups/csinla/servermedia/servermedia_`date +%Y%m%d_%H%M%S`.tar.gz /var/www/csinla/csinla/servermedia/
python /var/www/csinla/csinla/daily_task.py