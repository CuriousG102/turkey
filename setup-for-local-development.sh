#!/usr/bin/env bash
initdb /usr/local/var/postgres;
pg_ctl -D /usr/local/var/postgres -l logfile start;
sleep 3;
createdb turkey;
psql -h localhost -p 5432 -U $USER -d postgres -c "
CREATE USER django WITH PASSWORD 'django';
ALTER ROLE django SET client_encoding TO 'utf8';
ALTER ROLE django SET default_transaction_isolation TO 'read committed';
ALTER ROLE django SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE turkey TO django;
";
psql -h localhost -p 5432 -U $USER -d postgres -c "
ALTER USER django CREATEDB;
";
DJANGO_SETTINGS_MODULE=turkey.settings;
DATABASE_URL=postgres://django:django@localhost:5432/turkey;
STATIC_FOLDER=/usr/build/app/static;
DEBUG=1;
export DJANGO_SETTINGS_MODULE DATABASE_URL STATIC_FOLDER DEBUG;
python web/turkey/manage.py migrate;
