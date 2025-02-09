import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

#from parcer import run_parcer

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


def get_markets_ord_by_state_desc():
    stmnt = f"""select m.market_id, market_name, state_name
        from markets m
        join market_states ms on ms.market_id = m.market_id
        join states s on s.state_id = ms.state_id
        order by state_name desc;
        """
    res = request_db(stmnt)
    print(*res, sep='\n')


def get_markets_ord_by_state_asc():
    stmnt = f"""select m.market_id, market_name, state_name
        from markets m
        join market_states ms on ms.market_id = m.market_id
        join states s on s.state_id = ms.state_id
        order by state_name asc;
        """
    res = request_db(stmnt)
    print(*res, sep='\n')

def get_markets_ord_by_city_desc():
    stmnt = f"""select m.market_id, market_name, city_name
        from markets m
        join market_cities mc on mc.market_id = m.market_id
        join cities c on c.city_id = mc.city_id
        order by city_name desc;
        """
    res = request_db(stmnt)[0]
    print(res)


def get_markets_ord_by_city_asc():
    stmnt = f"""select m.market_id, market_name, city_name
        from markets m
        join market_cities mc on mc.market_id = m.market_id
        join cities c on c.city_id = mc.city_id
        order by city_name asc;
        """
    res = request_db(stmnt)
    print(*res, sep='\n')

def get_market_info_by_id(id):
    stmnt = f"""select market_name, state_name, city_name, date_start, date_end, day_of_week, time_start, time_end
        from markets m
        join market_states ms on m.market_id = ms.market_id
        join states s on s.state_id = ms.state_id
        join market_cities mc on m.market_id = mc.market_id
        join cities c on mc.city_id = c.city_id
        join market_season mss on mss.market_id = m.market_id
        join seasons ss on ss.season_id = mss.season_id
        where m.market_id = {id};
        """
    res = request_db(stmnt)[0]
    print("does it works?")
    print(*res, sep="\n")

menu_main = ["MENU:", "-------------------", "(MC)Markets group by city", "(MS)Markets group by state", "(S)tate's", "(C)ity's markets", "(E)xit"]
menu_market = ["Enter market ID or (e) for exit"]

while True:
    print(*menu_main, sep="\n")
    step = input("Make a choise: ").lower().strip()
    if step == "mc":
        get_markets_ord_by_city_asc()
        while True:
            print(menu_market)
            step = input("Make a choise: ")
            if step == "e":
                break
            else:
                try:
                    get_market_info_by_id(int(step))
                except TypeError:
                    print(menu_market)
    elif step == "ms":
        get_markets_ord_by_state_asc()
        while True:
            print(menu_market)
            step = input("Make a choise: ")
            if step == "e":
                break
            else:
                try:
                    get_market_info_by_id(int(step))
                except TypeError:
                    print(menu_market)
    elif step == "c":
        pass
    elif step == "s":
        pass
    elif step == "e":
        break




#get_markets_ord_by_state_desc()

#get_markets_ord_by_state_asc()

#get_markets_ord_by_city_desc()

#get_markets_ord_by_city_asc()






#changes to DB needs to be commited "conn.commit()" to see it right now