from flask import Flask

from main import app


@app.route('/movie/<title>')
def movie_title(title):
    pass


@app.route('/movie/year/to/year/<year>')
def movie_year_to_year(year):
    pass


@app.route('/rating/<str>')
def movie_rating(rating):
    pass


@app.route('/genre/<genre>')
def movie_genre(genre):
    pass
