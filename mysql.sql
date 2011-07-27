create table data(
  id int(11) not null auto_increment, 
  url varchar(100) not null, 
  localpath varchar(100) not null, 
  checksum varchar(36) not null, 
  created int(15) not null comment "unix timestamp",
  spidername varchar(15) not null,
  primary key(id),
  key(url)
)engine=innodb default charset=utf8;
