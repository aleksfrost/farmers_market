import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from parcer import run_parcer

from CONST import USER, PASS, HOST, DB_NAME, PORT

connection = psycopg2.connect(
    user=USER,
    password=PASS,
    host=HOST,
    port=PORT,
    database=DB_NAME
)

connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

#Выполнение запроса в БД
def request_db(stmnt):
    cursor = connection.cursor()
    cursor.execute(stmnt)
    record = cursor.fetchall()
    cursor.close()
    connection.close
    return record


def get_markets_ord_by_state():
    stmnt = f"""select m.market_id, market_name, state_name
        from markets m
        join market_states ms on ms.market_id = m.market_id
        join states s on s.state_id = ms.state_id
        order by state_name;
        """
    res = request_db(stmnt)
    #print(f'record is {type(res)}')
    print(*res, sep='\n')


get_markets_ord_by_state()

#changes to DB needs to be commited "conn.commit()" to see it right now