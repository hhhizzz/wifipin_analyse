from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from exts import db
from models import *

from web_core import app

manager = Manager(app)

## 绑定app和db 实现快捷数据库迁移
migrate = Migrate(app, db)

manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()
