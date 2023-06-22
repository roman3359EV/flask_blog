from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from blog import create_app
from config import DevelopConfig
from blog.models import db

app = create_app(DevelopConfig)
csrf = CSRFProtect(app)
db.init_app(app)
migrate = Migrate(app, db)

# TODO: CI/CD - docker swarm, kubernetes
# TODO: redis cache, main page, search, model events, websocket, kafka queue, mongo db, logging, clickhouse for log
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
