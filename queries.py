# pylint: disable=C0103, missing-docstring

def detailed_movies(db):
    '''return the list of movies with their genres and director name'''
    query = """
        SELECT
            movies.title,
            movies.genres,
            directors.name
        FROM movies
        JOIN directors ON movies.director_id = directors.id
    """
    db.execute(query)
    movies = db.fetchall()
    return movies

def late_released_movies(db):
    '''
    Retrieve a list of all movies released after the death of their respective directors.
    '''
    query = """
        SELECT movies.title
        FROM directors
        JOIN movies ON directors.id = movies.director_id
        WHERE (movies.start_year - directors.death_year) > 0
        ORDER BY movies.title
    """
    db.execute(query)
    result_set = db.fetchall()
    movie_titles = [movie[0] for movie in result_set]
    return movie_titles

def stats_on(db, genre_name):
    '''
    Retrieve statistics for a given movie genre and return them as a dictionary.
    '''
    query = """
        SELECT
            genres,
            COUNT(*) AS movie_count,
            ROUND(AVG(minutes), 2) AS average_length
        FROM movies
        WHERE genres = ?
    """
    db.execute(query, (genre_name,))
    genre_stats = db.fetchone()
    print(genre_stats)

    return {
        "genre": genre_stats[0],
        "number_of_movies": genre_stats[1],
        "avg_length": genre_stats[2]
    }

def top_five_directors_for(db, genre_name):
    '''
    Retrieve the top 5 directors with the most movies in a given genre and return them as a list.
    '''
    query = """
        SELECT
            directors.name AS director_name,
            COUNT(*) AS movie_count
        FROM movies
        JOIN directors ON movies.director_id = directors.id
        WHERE movies.genres = ?
        GROUP BY director_name
        ORDER BY movie_count DESC, director_name
        LIMIT 5
    """
    db.execute(query, (genre_name,))
    top_directors = db.fetchall()

    return top_directors

def movie_duration_buckets(db):
    '''return the movie counts grouped by bucket of 30 min duration'''
    query = '''SELECT movies.minutes/30 AS bin,
                COUNT(*) AS count
                FROM movies
                GROUP BY bin'''
    db.execute(query)
    results = db.fetchall()
    results.pop(0)
    index= [result[0]*30 for result in results]
    count = [result[1] for result in results]
    final_list = [((index[i]+30), count[i]) for i in range(0, len(index))]
    print(final_list)
    return final_list

def top_five_youngest_newly_directors(db):
    '''return the top 5 youngest directors when they direct their first movie'''
    query = '''SELECT directors.name, (m.start_year - directors.birth_year) AS age
                FROM movies as m
                LEFT JOIN directors ON m.director_id = directors.id
                WHERE age BETWEEN 1 AND 88
                ORDER BY age
                LIMIT 5'''
    db.execute(query)
    results = db.fetchall()
    print(results)
    return results
