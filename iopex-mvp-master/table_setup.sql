create table crawl_urls(
	id int not null auto_increment,
	create_date timestamp default current_timestamp,
	url varchar(256),
	flag varchar(15),
	company_name varchar(100),
	ats varchar(100),
	primary key (id)
	
);