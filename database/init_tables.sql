create table Inspector (
    id integer primary key autoincrement,
    name text not null,
    email text not null unique check(
        email like '%_@__%.com'
    )
);

create table Qualification (
    code text primary key not null
);

create table Inspector_Qualification (
    inspector_id integer,
    qualification_code text,
    primary key (inspector_id, qualification_code),
    -- deletes all qualifications associated with an inspector if the inspector is deleted
    foreign key (inspector_id) references Inspector(id) on delete cascade,
    -- deletes all records in Inspector_Qualification if a qualification code is deleted from Qualification table
    foreign key (qualification_code) references Qualification(code) on delete cascade
);

create table Building_Consent(
    bc_number integer primary key,
    level text not null,
    location text not null
);

create table Inspection (
    id integer primary key autoincrement,
    bc_number integer not null,
    description text not null,
    date text,
    time text,
    inspector_id integer,
    status text check (status in ('Scheduled', 'Passed', 'Failed', 'Cancelled')),
    -- delete all related inspections if a building consent is deleted
    foreign key (bc_number) references Building_Consent(bc_number) on delete cascade,
    -- set inspector_id to null if refernced inspector id deleted
    foreign key (inspector_id) references Inspector(id) on delete set null
    )
