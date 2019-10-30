from crontab import CronTab

cron = CronTab(user='bstroebl')
job = cron.new(command='python script.py')
job.minute.every(1)

cron.write()
