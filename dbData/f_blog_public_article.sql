create table article
(
    id          serial
        primary key,
    title       varchar(100),
    body        varchar,
    author      varchar(100),
    create_date timestamp with time zone
);

alter table article
    owner to postgres;

INSERT INTO public.article (id, title, body, author, create_date) VALUES (1, 'New Article medium', 'The body of the Article', 'Sam Soot', '2022-01-25 14:27:17.713000 +00:00');
INSERT INTO public.article (id, title, body, author, create_date) VALUES (2, 'Wading rivers is more diffcult than it looksd.', 'Some more text goes here.', 'Bill Boss', '2022-01-25 14:28:08.184000 +00:00');
INSERT INTO public.article (id, title, body, author, create_date) VALUES (3, 'Dogs who swim and those who don''t', 'Some are some aren''t', 'wadetheriver', '2022-01-25 14:28:54.453000 +00:00');
INSERT INTO public.article (id, title, body, author, create_date) VALUES (4, 'Just for fun', 'Here we are.', 'Scribbledfields', '2022-01-25 14:29:38.447000 +00:00');
