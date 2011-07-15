drop table if exists gla;
drop table if exists gumtree;
drop table if exists craigslist;
create table gla(
  id int(11) not null auto_increment,
  url varchar(100) not null,
  localpath varchar(500) not null,
  checksum varchar(32) not null,
  created int(11) not null comment "unix timestamp",
  primary key(id),
  key (url)
) engine=innodb default charset=utf8;

create table gumtree(
  id int(11) not null auto_increment,
  url varchar(100) not null,
  localpath varchar(500) not null,
  checksum varchar(32) not null,
  created int(11) not null comment "unix timestamp",
  primary key(id),
  key (url)
) engine=innodb default charset=utf8;
create table craigslist(
  
  id int(11) not null auto_increment,
  url varchar(100) not null,
  localpath varchar(500) not null,
  checksum varchar(32) not null,
  created int(11) not null comment "unix timestamp",
  primary key(id),
  key (url)
) engine=innodb default charset=utf8;

