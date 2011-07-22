create table data(
  id int(11) not null autoincrement, 
  url varchar(100) not null, 
  localpath varchar(100) not null, 
  checksum varchar(32) not null, 
  created int(11) not null comment "unix timestamp",
  spidername varchar(15) not null,
  primary key(id),
  key(url)
)engine=innodb default charset=utf8;
