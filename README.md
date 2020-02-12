App to tracking seen/unseen movies.
Build on TMDB

Look at http://kinobase.pp.ua


## Использование образа postgres от Bitnami.

Хелп тут
https://docs.bitnami.com/virtual-machine/infrastructure/postgresql/

Настройка образа Bitnami для dev базы postgres:

- open postresql port

        # sudo ufw allow 5432

- создаем базу

        # createdb -U postgres DATABASE_NAME  -O USER_NAME
        
- (факультативно) создаем юзера

        # createuser -U postgres USER_NAME -S -D -R -P
   
- add to /opt/bitnami/postgresql/data/pg_hba.conf as root. Если работаем от кастомного юзера, меняем postgres на юзера

        host DATABASE_NAME postgres all md5

- restart

        # cd /opt/bitnami
        # ./ctrlscript restart
