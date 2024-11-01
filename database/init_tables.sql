create table Inspector (
    id serial primary key,
    name text not null,
    email text not null unique check(
        email like '%_@__%.com'
    )
    residentail_qual text not null,
    commercial_qual text not null
);

create table Building_Consent(
    bc_number serial primary key,
    level text not null,
    location text not null
);

create table Inspection (
    id serial primary key,
    bc_number integer not null,
    description text not null,
    date text, --YR/MM/DD format
    time text, -- HH:MM format
    inspector_id integer,
    status text check (status in ('Scheduled', 'Passed', 'Failed', 'Cancelled')),
    --specifies order of inspection for a buidling consent
    order integer not null, 
    -- delete all related inspections if a building consent is deleted
    foreign key (bc_number) references Building_Consent(bc_number) on delete cascade,
    -- set inspector_id to null if refernced inspector id deleted
    foreign key (inspector_id) references Inspector(id) on delete set null
);
