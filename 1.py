import psycopg2


try:
    conn = psycopg2.connect(host="localhost", database="ytvideo", user="postgres", password="postgres", port="5438")


except Exception as ex:
    print(ex)
    exit(0)

# cur = conn.cursor()
# cur.execute("select * from url")