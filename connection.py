import psycopg2

try:
    conn = psycopg2.connect(host="localhost",
                            database="ytvideo",
                            user="postgres",
                            password="postgres",
                            port="5438")
    cur = conn.cursor()
    conn.autocommit = True


except Exception as ex:
    print(ex)
    exit(0)