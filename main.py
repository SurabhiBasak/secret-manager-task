import pandas as pd
import pyodbc
from google.cloud import secretmanager
from google.oauth2 import service_account


credentials = service_account.Credentials.from_service_account_file('/path/to/key.json')
client = secretmanager.SecretManagerServiceClient(credentials=credentials)

name = f"projects/flaskproject-341104/secrets/my-secret-password/versions/1"
response = client.access_secret_version(request={"name": name})

secret_password = response.payload.data.decode("UTF-8")

conn_str = (
    "DRIVER={PostgreSQL Unicode};"
    "DATABASE=test;"
    "UID=postgres;"
    "PWD=" + secret_password + ";"
    "SERVER=35.192.67.96;"
    "PORT=5432;"
    )


with pyodbc.connect(conn_str) as con:
    print(pd.read_sql("SELECT name from entries",con=con))
