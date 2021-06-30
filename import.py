import csv, os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


# Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine("postgresql://hqarjmdepnhngt:878b24ec455373807866474ef4b0bcac6f9dd1248e163a61f8ac77bd14c8d556@ec2-52-4-111-46.compute-1.amazonaws.com:5432/d2mjumqpqcetd3")
db = scoped_session(sessionmaker(bind=engine))

def main():
    temp = open ("data_csv/suppliers.csv")
    reader = csv.reader(temp)
    ctr = 1;

    for sup_id, sup_name, menu_code, top_id, p_small, p_large in reader:

        #print(ord_time[0])
        #db.execute("INSERT INTO menu (menu_code, menu_name) VALUES (:menu_code, :menu_name)",
        #     {"menu_code":ctr, "menu_name": menu_name[0]})
        #db.execute("INSERT INTO topping (top_id, top_name) VALUES (:top_id, :top_name)",
        #    {"top_id":ctr, "top_name": top_name[0]})
        #db.execute("INSERT INTO price (menu_code, top_id, p_small, p_large) VALUES (:menu_code, :top_id, :p_small, :p_large)",
        #     {"menu_code":menu_code, "top_id": top_id,"p_small":p_small, "p_large": p_large})
        #db.execute("INSERT INTO customer (cus_id, cus_name) VALUES (:cus_id, :cus_name)",
        #         {"cus_id":ctr, "cus_name": cus_name[0]})
        # db.execute("INSERT INTO orders (order_id, cus_id, ord_time) VALUES (:order_id, :cus_id, :ord_time)",
        #     {"order_id":ctr, "cus_id": int(cus_id), "ord_time":ord_time})
        # db.execute("INSERT INTO order_details (order_id, menu_code, top_id, price) VALUES (:order_id, :menu_code, :top_id, :price)",
        #     {"order_id":int(order_id), "menu_code": int(menu_code), "top_id" :int(top_id), "price" :price})
        db.execute("INSERT INTO Supplier (sup_id, sup_name, menu_code, top_id, p_small, p_large) VALUES (:sup_id, :sup_name, :menu_code, :top_id, :p_small, :p_large)",
             {"sup_id":int(sup_id), "sup_name" :sup_name, "menu_code" :int(menu_code), "top_id" :int(top_id), "p_small" :p_small, "p_large" :p_large})

        ctr +=1
        print("{}".format(ctr))
    db.commit()

if __name__ == "__main__":
    main()
