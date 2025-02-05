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

# try to connect to server and create DB_NAME

connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

def create_db():
    print()
    print("Create DB")
    try:
        with connection.cursor() as conn:
            sql_create_db = f'create database {DB_NAME}'
            conn.execute(sql_create_db)
            print("DB created!")
    except (Exception, Error) as error:
        print("Ошибка при создании базы данных", error)
    finally:
        if connection:
            conn.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")


#Выполнение запроса в БД
def make_request(request):
    with connection.cursor() as conn:
        conn.execute(request)
        return conn


#Start generating tables
def generate_tables():
    print()
    print("Sart creating tables")
    make_request("saql_to_generate_tables.sql")
    print()

#Start parcing
def parcing_export_file():
    print()
    print("Start parcing...")
    run_parcer()
    print()
    print("Done")




record = make_request(
    f"""select market_id, market_name, country_name, city_name
        from markets
        join zips on markets.zip_id=zips.zip_id
        join countries on zips.zip_id=countries.zip_id
        join cities on zips.zip_id=cities.zip_id
        where "country_id"=2;
        """
    ).fetchall()
print()
print()
for rec in record:
    print(rec)
print()
print(record)
print()
print()



if connection:
    connection.close()
    print("Connection with PostgreSQL is closed")


#changes to DB needs to be commited "conn.commit()" to see it right now