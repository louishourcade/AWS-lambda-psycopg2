import psycopg2


def handler(event, context):
    """Function that checks whether psycopg2 is succesfully imported or not"""

    return {"Status": "psycopg2 successfully imported"}
