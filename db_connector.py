import snowflake.connector


def get_connection():
    return snowflake.connector.connect(
        user='SNOWFLAKE_USERNAME',
        password='SNOWFLAKE_PASSWORD',
        account='SNOWFLAKE_ACCOUNT'
    )
