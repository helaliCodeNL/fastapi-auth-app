import sys
try:
    import psycopg2
except Exception as e:
    print('psycopg2 import error:', e)
    sys.exit(0)
try:
    conn = psycopg2.connect('postgresql://postgres:123321@localhost:5432/fastapi_auth')
    cur = conn.cursor()
    cur.execute('SELECT 1;')
    print('connected')
    cur.close()
    conn.close()
except Exception as e:
    print('connect error:', repr(e))
