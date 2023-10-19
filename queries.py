# pylint: disable=C0103, missing-docstring

def detailed_movies(db):
    '''return the list of movies with their genres and director name'''
    query = """
    SELECT m.title, m.genres, d.name
           FROM movies AS m
           JOIN directors AS d ON m.director_id = d.id
    """

    db.execute(query)
    results = db.fetchall()

    return results


def late_released_movies(db):
    '''return the list of all movies released after their director death'''
    query = """
     SELECT m.title
            FROM directors AS d
            INNER JOIN movies AS m
            ON d.id = m.director_id
            WHERE d.death_year <m.start_year
    """

    db.execute(query)
    results = db.fetchall()

    return [row[0] for row in results]


def stats_on(db, genre_name):
    '''return a dict of stats for a given genre'''
    query = f"""SELECT m.genres, COUNT(*), SUM(m.minutes) / COUNT(*)
                FROM movies as m
                WHERE m.genres LIKE "%{genre_name}%"""
    db.execute(query)
    results = db.fetchall()
    result_dict = {
        'genre': genre_name,
        'number of movies': results[0][1],
        'avg_length': results[0][2]
    }
    print(result_dict)
    return result_dict

def top_five_directors_for(db, genre_name):
    """return the top 5 of the directors with the most movies for a given genre"""
    query = """
    SELECT directors.name, COUNT(*) as director_count
    FROM movies as m
    LEFT JOIN directors ON m.director_id = directors.id
    WHERE m.genres LIKE "%ACTION%"
    GROUP BY directors.name
    ORDER BY director_count DESC
    LIMIT 5
"""
    db.execute(query)
    results = db.fetchall()

    return results

def movie_duration_buckets(db):
    '''return the movie counts grouped by bucket of 30 min duration'''
    pass  # YOUR CODE HERE


def top_five_youngest_newly_directors(db):
    '''return the top 5 youngest directors when they direct their first movie'''
    pass  # YOUR CODE HERE
