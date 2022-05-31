from flask import Flask, jsonify
import utils

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def main():
    return 'Так-то лучше'


@app.route('/movie/<title>/')
def get_film_by_title(title):
    return get_film_by_title(title)


@app.route('/movie/<int:first_year>/to/<int:second_year>')
def get_film_from_year_ro_year(first_year, second_year):
    return jsonify(utils.get_films_from_year_to_year(first_year, second_year))


@app.route('/rating/<category>/')
def get_group_by_rating(category):
    return jsonify(utils.get_films_by_rating(category))


@app.route('/genre/<genre>')
def get_films_by_genre(genre):
    return jsonify(utils.get_films_by_genre(genre))



if __name__ == "__main__":
    app.run(debug=True)
