FROM postgres:latest

COPY create_table.sql /docker-entrypoint-initdb.d/1_create_table.sql
COPY function.sql /docker-entrypoint-initdb.d/2_function.sql
