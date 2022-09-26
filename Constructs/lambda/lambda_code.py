import psycopg2

def handler(event,context):
    print(f"psycopg2 successfully imported")

    return {
        "Status": "SUCCESS"
    }

if __name__=="__main__":
    handler(None,None)