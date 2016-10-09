drop table if exists entries;
create table titanic (
	Embarked text,
	Sex text not null,
	Survived int not null,
	Number_of_siblings_and_spouses_aboard int,
	Passenger_id num not null,
	Class int not null,
	Cabiin int ,
	Fare num,
	Name text not null,
	Age int,
	Number_of_parents_and_children_aboard int,
	Ticket_number text
);