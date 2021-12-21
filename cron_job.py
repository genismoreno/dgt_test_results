from crontab import CronTab

with CronTab(user='genis') as cron:
    job = cron.new(command='/home/genis/projects/dgt_test_results/.env/bin/python /home/genis/projects/dgt_test_results/main.py --cron')
    job.minute.every(1)
    cron.write()
