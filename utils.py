import sqlite3
from collections import Counter
from pprint import pprint as pp


# Курсор - объект по результатам соединения "title": "title",
# "country": "country",
# "release_year": 2021,
# "genre": "listed_in",
# "description": "description"
# Курсор передаёт команды от приложения к базе данных и в обратку

# SELECT - позволяет выбрать, какие данные нам нужны
# Двойные кавычки используются для указания столбцов


def execute_query(query):
    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
    return result


def get_film_by_title(film_title):
    sqlite_query = f"""
                   SELECT title, country, release_year, listed_in, description
                   FROM netflix
                   WHERE type != 'TV Show'
                   AND title like '%{film_title}%' 
                   ORDER by release_year DESC
                   """
    info = execute_query(sqlite_query)
    search_result = {
	    "title": info[0],
	    "country": info[1],
	    "release_year": info[2],
	    "genre": info[3],
	    "description": info[4]
        }
    return search_result


def get_films_from_year_to_year(first_year, second_year):
    sqlite_query = f"""
                   SELECT title, `release_year` FROM netflix 
                   WHERE `release_year` BETWEEN {first_year} AND {second_year} 
                   ORDER BY `release_year` 
                   LIMIT 100 
                   """
    info = execute_query(sqlite_query)
    result_list = []
    for item in info:
        result_list.append({'title': item[0], 'release_year': item[1]})
    return result_list

def get_films_by_rating(category):
    rating_parameters = {'children': "'G'",
                         'family': "'G', 'PG', 'PG-13'",
                         'adult': "'R', 'NC-17'"}
    if category not in rating_parameters:
        return "Неверно введён рейтинг"
    else:
        sqlite_query = f"""
                    SELECT `title`, `rating`, `description`
                    FROM netflix 
                    WHERE `rating` in ({rating_parameters[category]})
                    ORDER BY `title`
        """
        info = execute_query(sqlite_query)
        result_list = []
        for item in info:
            result_list.append({'title': item[0], 'rating': item[1], 'desription': item[2]})
        return result_list

        # Почему-то в обратном порядке тут добавляются title, rating и description
        # Отключить сортировку ключей

def get_films_by_genre(genre):
    sqlite_query = f"""
                   SELECT title, description, release_year
                    FROM netflix 
                   WHERE listed_in LIKE '%{genre}%'
                   ORDER BY release_year DESC 
                   lIMIT 10                  
    """
    info = execute_query(sqlite_query)
    result_list = []
    for item in info:
        result_list.append({'title': item[0], 'description': item[1], 'release_year': item[2]})
        # Тут уж раз самые свежие фильмы нужны, пусть выводит год выпуска
    return result_list


def get_partners(first_actor, second_actor):
    sqlite_query = f"""
                SELECT `cast` FROM netflix 
                WHERE `cast` LIKE '%{first_actor}%' AND `cast` LIKE '%{second_actor}%' 
                """
    info = execute_query(sqlite_query)
    matches = []
    for cast in info:
        matches.extend(cast[0].split(', '))
    counter = Counter(matches)
    result_list = []
    for actor, count in counter.items():
        if actor not in [first_actor, second_actor] and count > 2:
            result_list.append(actor)
    return result_list


def get_film_by_parameters(movie_type, release_year, genre):
    query = f"""
                SELECT title, description FROM netflix 
                WHERE type = '{movie_type}'
                AND release_year = {release_year}
                AND listed_in LIKE '%{genre}%'
                """
    info = execute_query(query)
    result_list = []
    for movie in info:
        result_list.append({'title': movie[0], 'description': movie[1]})
    return result_list



#pp(get_film_by_title('100'))
#pp(get_films_from_year_to_year(2000, 2010))
#pp(get_films_by_rating('children'))
#pp(get_films_by_genre('Dramas'))
#pp(get_partners('Rose McIver', 'Ben Lamb'))
pp(get_film_by_parameters('Movie', 2000, 'Dramas'))
