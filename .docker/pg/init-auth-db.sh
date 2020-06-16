#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "postgres" --dbname "postgres" <<-EOSQL
    alter user postgres createdb;
    CREATE DATABASE auth;
    GRANT ALL PRIVILEGES ON DATABASE auth TO postgres;
EOSQL


psql -v ON_ERROR_STOP=1 --username "postgres" --dbname "postgres" <<-EOSQL
    alter user postgres createdb;
    CREATE DATABASE auth_test;
    GRANT ALL PRIVILEGES ON DATABASE auth_test TO postgres;
EOSQL

