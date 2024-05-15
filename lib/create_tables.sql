create table team2.documents (
    id serial primary key,
    s3_path text unique
);

create table team2.chunks (
    id serial primary key,
    document_id int not null ,
    content text,
    constraint chunk_fk foreign key (document_id) references team2.documents (id)
);

create table team2.topics (
    id serial primary key,
    name text unique
);

create table team2.chunk_topic (
    chunk_id int,
    topic_id int,
    constraint chunk_id_fk foreign key (chunk_id) references team2.chunks (id),
    constraint topic_id_fk foreign key (topic_id) references team2.topics (id),
    constraint chunk_topic_pk primary key (chunk_id, topic_id)
);


-- select distinct document_id
-- from team2.chunk_topic a
-- join team2.topics b on a.topic_id = b.id
-- join team2.chunks c on a.chunk_id = c.id
-- join team2.documents d on c.document_id = d.id
-- where b.name = 'players'
-- order by document_id desc