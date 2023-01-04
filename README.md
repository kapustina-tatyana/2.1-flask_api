
Для создания БД, выполнить в консоли:
```shell
createdb -Upostgres flask_api
```
Для создания таблиц в этой БД, выполнить в консоли:
```shell
python << EOF
from app import db
db.create_all()
EOF
```