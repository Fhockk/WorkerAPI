from app import db, app
from app.models import User

app.app_context().push()

# Создание пользователя с ролью админа (может создавать appointment)
admin = User()
admin.first_name = "AdminFirstName"
admin.last_name = "AdminLastName"
admin.email = "admin@example.com"
admin.password = "admin_password"
admin.is_admin = True
admin.gender_id = 1
db.session.add(admin)

# Создание пользователя с ролью менеджера (может все)
manager = User()
manager.first_name = "ManagerFirstName"
manager.last_name = "ManagerLastName"
manager.email = "manager@example.com"
manager.password = "manager_password"
manager.is_manager = True
admin.is_admin = True
manager.gender_id = 1
db.session.add(manager)

db.session.commit()
