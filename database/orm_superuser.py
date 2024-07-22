from database.models import Users
from sqlalchemy import select, update
import subprocess
from sqlalchemy import engine_from_config, URL
from sqlalchemy import pool
from environs import Env

env = Env()
env.read_env('.env')
host = env.str("DB_HOST"),
password = env.str("POSTGRES_PASSWORD"),
username = env.str("POSTGRES_USER"),
database = env.str("POSTGRES_DB"),
port = 5432

def set_backup(session):
    backup_command = f'pg_dump -U {username} -d {database} > {"backup.sql"}'
    subprocess.run(backup_command, shell=True)