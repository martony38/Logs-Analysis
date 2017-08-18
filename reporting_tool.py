#!/usr/bin/env python3

import psycopg2

DBNAME = 'news'


def most_popular_three_articles():
    ''' 1. What are the most popular three articles of all time? Which
           articles have been accessed the most? Present this
           information as a sorted list with the most popular article
           at the top.

    Examples:
        "Princess Shellfish Marries Prince Handsome" — 1201 views
        "Baltimore Ravens Defeat Rhode Island Shoggoths" — 915 views
        "Political Scandal Ends In Political Scandal" — 553 views
    '''

    # Connect to database and fetch 3 most popular articles.
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(
        '''SELECT *
             FROM article_views
         ORDER BY views_num DESC
            LIMIT 3'''
    )
    articles = c.fetchall()
    db.close()

    # Output results.
    print('\nThe most popular three articles of all time are:\n')
    for article in articles:
        print('    "' + article[0] + '" - ' + str(article[1]) + ' views')
    print('\n')


def most_popular_authors():
    '''	2. Who are the most popular article authors of all time? That
           is, when you sum up all of the articles each author has
           written, which authors get the most page views? Present this
           as a sorted list with the most popular author at the top.

    Examples:
        Ursula La Multa — 2304 views
        Rudolf von Treppenwitz — 1985 views
        Markoff Chaney — 1723 views
        Anonymous Contributor — 1023 views
    '''

    # Connect to database and fetch author list ordered by views.
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(
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
    authors = c.fetchall()
    db.close()

    # Output results.
    print('\nThe most popular authors of all time are:\n')
    for author in authors:
        print('    ' + author[0] + ' - ' + str(author[1]) + ' views')
    print('\n')


def days_with_most_errors():
    '''	3. On which days did more than 1% of requests lead to errors?
           The log table includes a column status that indicates the
           HTTP status code that the news site sent to the user's
           browser.

    Example:
        July 29, 2016 — 2.5% errors
    '''

    # Connect to database and fetch percentage of bad requests per day.
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(
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
            WHERE 100.0 * bad_req_num / (bad_req_num + good_req_num) > 1
        '''
    )
    error_days = c.fetchall()
    db.close()

    # Output result
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


if __name__ == '__main__':
    most_popular_three_articles()
    most_popular_authors()
    days_with_most_errors()
