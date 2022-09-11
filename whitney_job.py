from apscheduler.schedulers.blocking import BlockingScheduler
from campsites import search_acceptable_dates

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=10)
def timed_job():
    print("Running Whitney search!")
    search_acceptable_dates()


sched.start()
