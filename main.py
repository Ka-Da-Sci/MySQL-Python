import mysql.connector as mysql
from mysql.connector import Error as ERROR

#Function that creates the specified MySQL database if not yet existing and then connects to it, otherwise just
# connects to it.
def create_connection(db_name):
    try:
        db = mysql.connect(host='localhost', user='root', password='YOUR_PASSWORD')
        cursor = db.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        db = mysql.connect(host='localhost', user='root', password='YOUR_PASSWORD', database=db_name)
    except ERROR as e:
        print(e)
    else:
        return db


if __name__ == "__main__":
    db = create_connection("Red30")
    cursor = db.cursor()

    #creates the specified table if not existing yet.
    cursor.execute("CREATE TABLE IF NOT EXISTS Sales_mysql_only_style (order_num INTEGER NOT NULL PRIMARY KEY UNIQUE "
                   "AUTO_INCREMENT, order_type VARCHAR(50), cust_name VARCHAR(50), prod_category VARCHAR(50), "
                   "prod_number VARCHAR(10), prod_name VARCHAR(50), quantity INTEGER, price FLOAT, discount FLOAT, "
                   "order_total FLOAT)")

    #Data to update the table with
    records = [
        {"order_type": "Rush", "cust_name": "Godwin", "prod_category": "Electronics", "prod_number": "L-15", "prod_name": "Laptop", "quantity": 1, "price": 500000, "discount": 5.60, "order_total": 472000},
        {"order_type": "Prepaid", "cust_name": "Marchiqa", "prod_category": "Apparel", "prod_number": "5F3", "prod_name": "Footwear", "quantity": 2, "price": 12500, "discount": 2.75, "order_total": 24312.5},
        {"order_type": "Return", "cust_name": "Lulu", "prod_category": "Beauty Care", "prod_number": "N100E", "prod_name": "Makeup", "quantity": 100, "price": 3500, "discount": 5.50, "order_total": 330750},
        {"order_type": "Prepaid", "cust_name": "Chommy", "prod_category": "Apparel", "prod_number": "S5M", "prod_name": "Polo", "quantity": 5, "price": 11000, "discount": 2.34, "order_total": 53713},
        {"order_type": "Rush", "cust_name": "Sybil", "prod_category": "Beauty Care", "prod_number": "N2N", "prod_name": "Cream", "quantity": 2, "price": 4500, "discount": 3.18, "order_total": 8713.8}
    ]

    #Updates the table "Sales_mysql_only_style" with a given data
    cursor.executemany(f'''INSERT INTO Sales_mysql_only_style({', '.join(records[0].keys())}) VALUES ({', '.join(['%s']*len(records[0]))})''', [tuple(record.values()) for record in records])
    cursor.execute(f'INSERT INTO Red30.Sales_mysql_only_style SELECT * FROM Red30.Sales')

    #Queries the database and reads the cust_name and associated order_total from Sales_mysql_only_style
    # table, grabbing the record(row) with the largest order_total.
    cursor.execute(f'SELECT cust_name, order_total FROM Sales_mysql_only_style ORDER BY order_total DESC LIMIT 1')
    print([row for row in cursor.fetchall()])

    # Queries the database and reads all records from the Sales_mysql_only_style table.
    cursor.execute("SELECT * FROM Sales_mysql_only_style")
    sales_records = [row for row in cursor.fetchall()]
    print(sales_records)


