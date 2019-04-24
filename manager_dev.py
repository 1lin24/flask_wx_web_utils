from flask_script import Manager,Server
from app import create_app, db, models
from flask_migrate import Migrate, MigrateCommand

app = create_app('dev')
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host='0.0.0.0', port='5099'))

@manager.shell
def make_shell_context():
    return dict(app=app, db=db, models=models)

if __name__ == '__main__':
    manager.run()
