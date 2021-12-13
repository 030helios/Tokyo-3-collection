create table shop(
    ID char(5) not null,
    itemname varchar(40) not null,
    category varchar(20) not null,
    stock int not null,
    price int not null,
    img_url varchar(200) not null,
    primary key (ID, itemname)
);

create table user(
    ID char(7) not null,
    username varchar(20) not null,
    pwd char(32) not null,
    phone char(10) not null,
    primary key (ID, username)
);

create table order_(
    orderID int not null,
    stat varchar(20) not null,
    orderer varchar(20) not null,
    category varchar(20) not null,
    itemname varchar(20) not null,
    time_start varchar(20) not null,
    time_end varchar(20) not null,
    order_amount int not null,
    primary key (orderID)
);
