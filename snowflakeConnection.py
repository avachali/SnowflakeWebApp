#Imports
from snowflake import connector
import os

#Snowflake stuff  - get sensitive deets from env variable
def sfConnect():
    cnx = connector.connect(
        account = os.getenv('SF_GCP_ACCNT'),
        user = os.getenv('SF_GCP_USR'),
        password = os.getenv('SF_GCP_PWD'),
        warehouse ='compute_wh',
        database='demo_db',
        schema='public',
        role='sysadmin')

    return cnx
