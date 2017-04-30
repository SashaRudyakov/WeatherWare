drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  'text' text not null
);

drop table if exists weather_test;
create table weather_test (
  id integer primary key autoincrement,
  day text not null,
  prediction text not null,
  wear text not null
);

insert into weather_test(day, prediction, wear) values ('Moonday', 'sunny?', 'many hats');
insert into weather_test(day, prediction, wear) values ('Saturday', 'big Rain', 'not many hats');
