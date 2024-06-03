import os
import threading
import time
import requests
import psycopg2
from dotenv import load_dotenv
from threading import Thread
from contextlib import contextmanager

# 1st Task

# pip install psycopg2
# pip install python-dotenv

load_dotenv()

conn = psycopg2.connect(database=os.getenv('database'),
                        user=os.getenv('user'),
                        password=os.getenv('password'),
                        host=os.getenv('host'),
                        port=os.getenv('port')
                        )

cur = conn.cursor()

create_table_query = """CREATE TABLE IF NOT EXISTS product(
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        price NUMERIC(10,2) NOT NULL,
        color VARCHAR(255) NOT NULL,
        image VARCHAR(255) NOT NULL
)"""
cur.execute(create_table_query)
conn.commit()


# conn.close()
# cur.close()


# -------------------------------------------------------------------------

# 2nd Task

def commit(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        conn.commit()
        return result

    return wrapper


@commit
def insert_product():
    try:
        name = input('Enter Product Name: ')
        price = input('Enter Product Price: ')
        color = input('Enter Product Color: ')
        image = input('Enter Product Image: ')
        insert_query = """Insert into product(name,price,color,image) values (%s,%s,%s,%s)"""
        cur.execute(insert_query, (name, price, color, image))
    except psycopg2.Error as e:
        conn.rollback()
        print(('Error', str(e)))
    finally:
        conn.close()
        cur.close()

    print('Product inserted successfully')


def select_all_products():
    try:
        cur.execute("SELECT * FROM product")
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except psycopg2.Error as e:
        conn.rollback()
        print(('Error', str(e)))


@commit
def update_product():
    _id = input('Enter Product ID: ')
    try:
        cur.execute("""select * from product where id = %s""", (_id,))
        row = cur.fetchone()
        if row:
            name = input('Enter Product Name: ')
            price = input('Enter Product Price: ')
            color = input('Enter Product Color: ')
            image = input('Enter Product Image: ')
            cur.execute("""UPDATE product SET name = %s,price = %s,color = %s,image = %s 
             where id=%s""", (name, price, color, image, _id))

            print('Product updated successfully')
        else:
            print("Product not found")
    except psycopg2.Error as e:
        conn.rollback()
        print(('Error', str(e)))
    finally:
        conn.close()
        cur.close()


@commit
def delete_product():
    _id = input('Enter Product ID: ')
    try:
        cur.execute("""DELETE FROM product WHERE id=%s""", (_id,))
        print('Product deleted successfully')
    except psycopg2.Error as e:
        conn.rollback()
        print(('Error', str(e)))
    finally:
        conn.close()
        cur.close()


# if __name__ == '__main__':
#     insert_product()
#     select_all_products()
#     update_product()
#     delete_product()
# -------------------------------------------------------------------------------------------------------------

# 3rd Task

class Alphabet:
    def __init__(self):
        self.letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            if self.index >= len(self.letters):
                raise StopIteration
            letter = self.letters[self.index]
            self.index += 1
            return letter
        except StopIteration:
            raise StopIteration


# if __name__ == '__main__':
#     alphabet = Alphabet()
#     for let in alphabet:
#         print(let)
# ----------------------------------------------------------------------------------------------------------------

# 4st Task

def print_number():
    for i in range(6):
        print(i)
        time.sleep(1)


def print_letter():
    letters = 'ABCDE'
    for i in letters:
        print(i)
        time.sleep(1)


thread1 = threading.Thread(target=print_number)
thread2 = threading.Thread(target=print_letter)


# thread1.start()
# thread2.start()
# thread1.join()
# thread2.join()

# ----------------------------------------------------------------------------------------------------------------

# 5st Task


class Product:
    def __init__(self, name, price, color, image):
        self.name = name
        self.price = price
        self.color = color
        self.image = image

    def save(self):
        try:
            insert_data_query = """INSERT INTO product(name,price,color,image) VALUES(%s,%s,%s,%s)"""
            cur.execute(insert_data_query, (self.name, self.price, self.color, self.image))
            conn.commit()
            print('Product saved successfully')
        except psycopg2.Error as e:
            conn.rollback()
            print(('Error', str(e)))
        finally:
            conn.close()
            cur.close()


# name1 = input('Enter Product Name: ')
# price1 = input('Enter Product Price: ')
# color1 = input('Enter Product Color: ')
# image1 = input('Enter Product Image: ')
# product = Product(name1, price1, color1, image1)
# product.save()

# -----------------------------------------------------------------------------------------------------------

# 6st Task

class Dbconnect:
    def __enter__(self):
        self.conn = psycopg2.connect(
            database=os.getenv('database'),
            user=os.getenv('user'),
            password=os.getenv('password'),
            host=os.getenv('host'),
            port=os.getenv('port')
        )
        self.cur = self.conn.cursor()
        print('Connected to PostgreSQL')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.conn.rollback()
        else:
            self.conn.commit()
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()


# with Dbconnect() as db:
#     conn = db.conn
#     cur = db.cur

# 2-usul
# @contextmanager
# def connect_db():
#     conn1 = None
#     cur1 = None
#
#     try:
#         conn1 = psycopg2.connect(database=os.getenv('database'),
#                                  user=os.getenv('user'),
#                                  password=os.getenv('password'),
#                                  host=os.getenv('host'),
#                                  port=os.getenv('port'))
#         cur1 = conn1.cursor()
#         yield conn1, cur1
#     except psycopg2.Error as e:
#         conn.rollback()
#         print(e)
#     finally:
#         conn1.close()
#         cur1.close()
#
#
# with connect_db() as (conn, cur):
#     print('Connected to PostgreSQL')

# --------------------------------------------------------------------------------------------------------
# 7-Task

url = 'https://dummyjson.com/products/'
response = requests.get(url)

create_table_products_query = """create table if not exists products(
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description TEXT ,
        price INT,
        discountPercentage FLOAT,
        rating FLOAT ,
        stock INT,
        brand VARCHAR(255) NOT NULL,
        category VARCHAR(255) NOT NULL,
        thumbnail VARCHAR,
        images jsonb
);"""

conn = psycopg2.connect(database=os.getenv('database'),
                        user=os.getenv('user'),
                        password=os.getenv('password'),
                        host=os.getenv('host'),
                        port=os.getenv('port')
                        )

cur = conn.cursor()
cur.execute(create_table_query)
conn.commit()

insert_into_query = """insert into products (title, description, price, discountPercentage, rating, stock, brand,
 category, thumbnail,images)

    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);

"""

for product in response.json()['products']:
    cur.execute(insert_into_query, (
        product['title'], product['description'], product['price'], product['discountPercentage'],
        product['rating'],
        product['stock'], product['brand'], product['category'], product['thumbnail'], str(product['images'])))
conn.commit()
conn.close()
cur.close()
