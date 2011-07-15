create table gla(id integer primary key autoincrement, url varchar(100) not null, localpath varchar(500) not null, checksum varchar(32) not null, created integer not null);
create table gumtree(id integer primary key autoincrement, url varchar(100) not null, localpath varchar(500) not null, checksum varchar(32) not null, created integer not null);
create table craigslist(id integer primary key autoincrement, url varchar(100) not null, localpath varchar(500) not null, checksum varchar(32) not null, created integer not null);
