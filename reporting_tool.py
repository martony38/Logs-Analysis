#!/usr/bin/env python3

import psycopg2

DBNAME = 'news'

''' 1. What are the most popular three articles of all time? Which
       articles have been accessed the most? Present this
       information as a sorted list with the most popular article
       at the top.

Examples:
    "Princess Shellfish Marries Prince Handsome" — 1201 views
    "Baltimore Ravens Defeat Rhode Island Shoggoths" — 915 views
    "Political Scandal Ends In Political Scandal" — 553 views
'''
most_popular_three_articles_query = (
    '''SELECT *
         FROM article_views
     ORDER BY views_num DESC
        LIMIT 3'''
)

''' 2. Who are the most popular article authors of all time? That
       is, when you sum up all of the articles each author has
       written, which authors get the most page views? Present this
       as a sorted list with the most popular author at the top.

Examples:
    Ursula La Multa — 2304 views
    Rudolf von Treppenwitz — 1985 views
    Markoff Chaney — 1723 views
    Anonymous Contributor — 1023 views
'''
most_popular_authors_query = (
    '''SELECT name, SUM(views_num) AS views_total
         FROM (SELECT name, views_num
                 FROM (SELECT name, title
                         FROM authors JOIN articles
                           ON articles.author = authors.id)
                   AS article_authors
                 JOIN article_views
                   ON article_authors.title = article_views.title)
           AS author_views
     GROUP BY name
     ORDER BY views_total DESC'''
)

''' 3. On which days did more than 1% of requests lead to errors?
       The log table includes a column status that indicates the
       HTTP status code that the news site sent to the user's
       browser.

Example:
    July 29, 2016 — 2.5% errors
'''
days_with_most_errors_query = (
    '''SELECT bad_requests.day,
              100.0 * bad_req_num / (bad_req_num + good_req_num)
              AS bad_requests_percentage
         FROM (SELECT day, requests_num AS good_req_num
                 FROM daily_requests
                WHERE status = '200 OK')
           AS good_requests
         JOIN (SELECT day, requests_num AS bad_req_num
                 FROM daily_requests
                WHERE status != '200 OK')
           AS bad_requests
           ON good_requests.day = bad_requests.day
        WHERE 100.0 * bad_req_num / (bad_req_num + good_req_num) > 1'''
)


def connect_database(db_name=DBNAME):
    try:
        db = psycopg2.connect(database=db_name)
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print('Unable to connect to database')
        print(e.pgerror)
        sys.exit(1)


def get_query_results(query):
    db, c = connect_database()
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


def print_results(question):
    if question == 'articles':
        articles = get_query_results(most_popular_three_articles_query)
        print('\nThe most popular three articles of all time are:\n')
        for article in articles:
            print('    "' + article[0] + '" - ' + str(article[1]) + ' views')
        print('\n')
    elif question == 'authors':
        authors = get_query_results(most_popular_authors_query)
        print('\nThe most popular authors of all time are:\n')
        for author in authors:
            print('    ' + author[0] + ' - ' + str(author[1]) + ' views')
        print('\n')
    elif question == 'error_days':
        error_days = get_query_results(days_with_most_errors_query)
        if error_days:
            if len(error_days) > 1:
                print('\nThe days on which more than 1% of requests led to '
                      'errors were:\n')
            else:
                print('\nThe day on which more than 1% of requests led to errors '
                      'was:\n')
            for error_day in error_days:
                print('    ' + '{:%B %d, %Y}'.format(error_day[0]) + ' - ' +
                      '{:.1f}'.format(error_day[1]) + '% errors')
        else:
            print('\nThere were no days on which more than 1% of requests led to '
                  'errors!')
        print('\n')
    else:
        print('I can not answer this question.')

if __name__ == '__main__':
    print_results('articles')
    print_results('authors')
    print_results('error_days')
