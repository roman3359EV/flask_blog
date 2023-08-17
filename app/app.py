from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from blog import create_app
from config import DevelopConfig
from blog.models import db, cache
from blog.events import socketio

app = create_app(DevelopConfig)
csrf = CSRFProtect(app)
db.init_app(app)
migrate = Migrate(app, db)
cache.init_app(app)
socketio.init_app(app)


# TODO: CI/CD - docker, docker swarm, kubernetes, health check in docker
# TODO: main page, search, kafka queue, clickhouse for log
if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5050)
    # app.run(debug=True, host='0.0.0.0', port=5050)
