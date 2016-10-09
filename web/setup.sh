#!/usr/bin/env bash
#these will error if there's already a database and user, but who cares...
psql -h postgres -p 5432 -U postgres -c "CREATE DATABASE turkey;"
psql -h postgres -p 5432 -U postgres -c "
CREATE USER django WITH PASSWORD 'django';
ALTER ROLE django SET client_encoding TO 'utf8';
ALTER ROLE django SET default_transaction_isolation TO 'read committed';
ALTER ROLE django SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE turkey TO django;
";
