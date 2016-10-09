drop table if exists entries;
create table entries (
	Embarked text,
	Sex text not null,
	Survived int not null,
	Number_of_siblings_and_spouses_aboard int,
	Passenger_id num not null primary key,
	Class int not null,
	Cabin int,
	Fare num,
	Name text not null,
	Age real,
	Number_of_parents_and_children_aboard int,
	Ticket_number text
);