# Logs Analysis

Source code for my third project for the [Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004) (FSWDN) program from Udacity.

This project is a single file python 3 program that fetch and summarizes data from a large [PostgreSQL](https://www.postgresql.org) database called _news_.

The database has 3 tables: [_authors_](#authors), [_articles_](#articles), and [_log_](#log) as well as 2 views created for this project: [_article_views_](#articles_views) and [_daily_requests_](#daily_requests).

## Installation
The instructions to download the database are part of the [FSWDN](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004) program and can be found [here](https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/262a84d7-86dc-487d-98f9-648aa7ca5a0f/concepts/a9cf98c8-0325-4c68-b972-58d5957f1a91).
Once the virtual machine and database are setup, do not forget to create the 2 required [views](#views) before running the program:
```
python3 reporting_tool.py
```

## Tables
### articles
The _articles_ table includes information about articles.
```
                                  Table "public.articles"
 Column |           Type           |                       Modifiers
--------+--------------------------+-------------------------------------------------------
 author | integer                  | not null
 title  | text                     | not null
 slug   | text                     | not null
 lead   | text                     |
 body   | text                     |
 time   | timestamp with time zone | default now()
 id     | integer                  | not null default nextval('articles_id_seq'::regclass)
Indexes:
    "articles_pkey" PRIMARY KEY, btree (id)
    "articles_slug_key" UNIQUE CONSTRAINT, btree (slug)
Foreign-key constraints:
    "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)
```
### authors
The _authors_ table includes information about the authors of articles.
```
                         Table "public.authors"
 Column |  Type   |                      Modifiers
--------+---------+------------------------------------------------------
 name   | text    | not null
 bio    | text    |
 id     | integer | not null default nextval('authors_id_seq'::regclass)
Indexes:
    "authors_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "articles" CONSTRAINT "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)
```
### log
The _log_ table includes one entry for each time a user has accessed the site.
```
                                  Table "public.log"
 Column |           Type           |                    Modifiers
--------+--------------------------+--------------------------------------------------
 path   | text                     |
 ip     | inet                     |
 method | text                     |
 status | text                     |
 time   | timestamp with time zone | default now()
 id     | integer                  | not null default nextval('log_id_seq'::regclass)
Indexes:
    "log_pkey" PRIMARY KEY, btree (id)
```

## Views
### article_views
This view gathers article titles with their respective number of views by joining tables _articles_ and _log_ on matching column _path_ from _log_ with column _slug_ from _articles_.
```
   View "public.article_views"
  Column   |  Type   | Modifiers
-----------+---------+-----------
 title     | text    |
 views_num | integer |
```
The following commands in the psql shell will create the view:
```
CREATE VIEW article_views AS
    SELECT title, CAST(COUNT(log.path) AS int) AS views_num
      FROM articles LEFT JOIN log
        ON log.path LIKE '%' || articles.slug
     WHERE status = '200 OK'
  GROUP BY title;
```

### daily_requests
This view gathers the number of requests grouped by status code for each day.
```
    View "public.daily_requests"
    Column    |  Type   | Modifiers
--------------+---------+-----------
 day          | date    |
 status       | text    |
 requests_num | integer |
```
Create it using the psql shell:
```
CREATE VIEW daily_requests AS
    SELECT CAST(time AS date) AS day, status, CAST(COUNT(*) AS int) AS requests_num
      FROM log
  GROUP BY (day,status);
```