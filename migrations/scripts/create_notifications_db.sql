select 'create database notifications' where not exists (select from pg_database where datname = 'notifications')\gexec
\c notifications
create schema if not exists notifications;
create schema if not exists announcements;
