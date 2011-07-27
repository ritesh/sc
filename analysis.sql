create table analysis(
  id int(11) not null auto_increment, 
  FK_data int(11) not null,
  sensitivity float(2,2) not null default 0 comment "Sensitivity, either 1, 2, 0.5",
  positive boolean not null default 0 comment "Does image contain steg content?",
  jsteg tinyint(3) not null default 0 comment "JSteg steganography",
  outguess tinyint(3) not null default 0 comment "Outguess Steganography",
  jphide tinyint(3) not null default 0 comment "JPHide Steganography",
  invsecrets tinyint(3) not null default 0 comment "Invisible Secrets steganography",
  f5 tinyint(3) not null default 0 comment "F5 steganography",
  appended tinyint(3) not null default 0 comment "Steg is appended",
  created int(15) not null comment "Unix TimeStamp",
  foreign key (FK_data) references data(id),
  primary key(id)
)engine=innodb default charset=utf8;
