from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

class MyScheduler:
    '''
    scheduler = MyScheduler().cfg_scheduler()
    scheduler.add_job(tick, 'cron', second='*/5')
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
    '''
    def cfg_scheduler(self):
        scheduler = BlockingScheduler()
        scheduler.add_jobstore(SQLAlchemyJobStore(url='sqlite:///jobs.db'))
        return scheduler
    