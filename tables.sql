CREATE DATABASE MyPizza;
USE MyPizza;
-- drop database MyPizza;

-- Table For Menu --
CREATE TABLE Menu(
	menu_code int auto_increment,
    menu_name VARCHAR(255),
    primary key (menu_code)
);

-- Table For Topping --
CREATE TABLE Topping(
	top_id int auto_increment,
    top_name VARCHAR(255),
    primary key (top_id)
);

-- Table For Customer --
CREATE TABLE Customer(
	cus_id int auto_increment,
    cus_name VARCHAR(255),
    primary key (cus_id)
);

-- Many to Many b/w Menu & Topping --
CREATE TABLE Price(
	menu_code int not null,
    top_id int not null,
    p_small float(10, 3) not null,
    p_large float(10, 3) not null,
    foreign key (menu_code) references Menu(menu_code),
    foreign key (top_id) references Topping(top_id),
    primary key (menu_code, top_id)
);

-- One to Many Relationship With Customer --
CREATE TABLE Orders(
	order_id int auto_increment,
    cus_id int not null,
    ord_time timestamp,
    foreign key (cus_id) references Customer(cus_id),
    primary key (order_id)
);

CREATE TABLE Order_details(
	order_id int not null,
    menu_code int not null,
    top_id int not null,
    price float(10, 3),
    foreign key (order_id) references Orders(order_id),
    foreign key (menu_code, top_id) references Price(menu_code, top_id),
    primary key (order_id, menu_code, top_id)
);

-- Stand Alone Supplier Table --
CREATE TABLE Supplier(
	sup_id int NOT NULL,
    sup_name VARCHAR(255),
    menu_code int not null,
    top_id int not null,
    p_small float(10, 3) not null,
    p_large float(10, 3) not null
);

INSERT INTO MENU VALUES (NULL, 'Regular Pizza'), (NULL, 'Special Pizza');
INSERT INTO Topping VALUE (NULL, 'Pepperoni'),
			(NULL, 'Sausage'), (NULL, 'Chicken');

INSERT INTO Price VALUES (1, 1, 12.5, 22.5), (1, 2, 15.5, 25.5), (1, 3, 12.6, 23.5),
				(2, 1, 10.5, 19.5), (2, 2, 22.5, 52.5), (2, 3, 22.6, 64.5);

INSERT INTO Customer VALUES (NULL, 'Ammar Alam'), (NULL, 'Basit'), (NULL, 'Hamza');

INSERT INTO Orders VALUES (NULL, 1, '2021-11-10'), (NULL, 1, '2021-11-10'),
							(NULL, 3, '2021-10-10'), (NULL, 3, '2021-09-10'),
							(NULL, 2, '2021-07-10');

SELECT * FROM Menu;
SELECT * FROM Topping;
SELECT * FROM Price;
SELECT * FROM Customer;
SELECT * FROM Orders;
SELECT * FROM Order_details;


INSERT INTO Order_details VALUES (1, 1, 1, 12.5), (2, 2, 1, 11.5), (3, 2, 3,  21.5);
INSERT INTO Order_details VALUES (4, 1, 1, 12.5);
INSERT INTO Order_details VALUES (4, 1, 1, 12.5);

INSERT INTO Supplier VALUES (1, "Alice", 1, 1, 9, 8), (1, "Alice", 1, 2, 12, 20),
							(1, 'Bubble', 2, 1, 5, 12);

-- Count Valuable Customer --
SELECT cus_id as Customer, count(order_id) as "Total Orders" FROM Orders group by cus_id;
-- Most Valuable Customer --
SELECT cus_id, count(ord_details.price) FROM Orders as ord
	INNER JOIN Order_details as ord_details
	on ord.order_id = ord_details.order_id
    group by cus_id
	Order by ord_details.price DESC LIMIT 5;

-- Highest Order Range --
SELECT ord_details.menu_code, ord_details.top_id, sum(ord_details.price) as "High Value Orders" FROM Orders as ord
	INNER JOIN Order_details as ord_details
	on ord.order_id = ord_details.order_id
    group by ord_details.menu_code, ord_details.top_id
	Order by sum(ord_details.price) DESC LIMIT 5;

SELECT * FROM Order_details;

-- Monthly Sales --
SELECT MONTH(ord.ord_time) as Month, price FROM Order_details as ord_details
	INNER JOIN Orders as ord
    on ord_details.order_id = ord.order_id
    group by MONTH(ord.ord_time);

-- Net Profit --
SELECT sup.menu_code, sup.top_id, (pt.p_small - sup.p_small) as small, (pt.p_large - sup.p_large) as Large
FROM Supplier as sup INNER JOIN Price as pt
ON (sup.menu_code = pt.menu_code) and (sup.top_id = pt.top_id);

-- Most Sold Pizza --
SELECT mn.menu_name as Menu, count(ord_details.menu_code) as "Total Orders" FROM Menu as mn
	INNER JOIN Order_details as ord_details
    on mn.menu_code = ord_details.menu_code
    group by mn.menu_code;

-- Most Use Topping --
SELECT tp.top_name as Topping, count(ord_details.top_id) as "Total Orders" FROM Topping as tp
	INNER JOIN Order_details as ord_details
    on tp.top_id = ord_details.top_id
    group by tp.top_name;

-- Count Valuable Supplier --
SELECT sup_name as "Supplier Name", count(sup.menu_code) FROM Supplier as sup
	INNER JOIN order_details as ord_details
	on (sup.menu_code = ord_details.menu_code) and (sup.top_id = ord_details.top_id)
	group by sup.sup_name;

-- Lifetime Order --
SELECT count(order_id) as "Total Orders" FROM Orders;
