import time
from flask_migrate import Migrate
from flask_apscheduler import APScheduler
from config import DevelopConfig
from blog import create_app
from blog.models import User, db

app = create_app(DevelopConfig)
db.init_app(app)
migrate = Migrate(app, db)

scheduler = APScheduler()
scheduler.init_app(app)


def first_job():
    with app.app_context():
        with open('log.txt', 'a') as f:
            pass
            # f.write("tick \n")
            # f.write(f"{User.query.first().name} \n")


def scheduler_job():
    scheduler.add_job(id='first_job_1', func=first_job, trigger='interval', seconds=3)
    scheduler.start()

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


if __name__ == '__main__':
    scheduler_job()
