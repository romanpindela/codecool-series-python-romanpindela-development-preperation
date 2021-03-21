from flask import Flask, render_template, url_for, redirect
from data import queries
import math
from dotenv import load_dotenv

from flask import jsonify, json
from flask import request
from flask import session

import random


load_dotenv()
app = Flask('codecool_series')
SHOWS_PER_PAGE = 15
SHOWN_PAGE_NUMBERS = 5 # should be odd to have a symmetry in pagination

@app.route('/')
def index():
    shows = queries.get_shows()
    return render_template('index.html', shows=shows)


@app.route('/design')
def design():
    return render_template('design.html')


@app.route('/shows/')
@app.route('/shows/<int:page_number>')
@app.route('/shows/most-rated/')
@app.route('/shows/most-rated/<int:page_number>')
@app.route('/shows/order-by-<order_by>/')
@app.route('/shows/order-by-<order_by>-<order>/')
@app.route('/shows/order-by-<order_by>/<int:page_number>')
@app.route('/shows/order-by-<order_by>-<order>/<int:page_number>')
def shows(page_number=1, order_by="rating", order="DESC"):
    count = queries.get_show_count()
    pages_count = math.ceil(count[0]['count'] / SHOWS_PER_PAGE)
    shows = queries.get_shows_limited(order_by, order, SHOWS_PER_PAGE, (page_number - 1) * SHOWS_PER_PAGE)

    shown_pages_start = int(page_number - ((SHOWN_PAGE_NUMBERS - 1) / 2))
    shown_pages_end = int(page_number + ((SHOWN_PAGE_NUMBERS - 1) / 2))
    if shown_pages_start < 1:
        shown_pages_start = 1
        shown_pages_end = SHOWN_PAGE_NUMBERS
    elif shown_pages_end > pages_count:
        shown_pages_start = pages_count - SHOWN_PAGE_NUMBERS + 1
        shown_pages_end = pages_count

    return render_template(
        'shows.html',
        shows=shows,
        pages_count=pages_count,
        page_number=page_number,
        shown_pages_start=shown_pages_start,
        shown_pages_end=shown_pages_end,
        order_by=order_by,
        order=order
    )

# list all show seasons
@app.route('/show/<int:id>')
@app.route('/show/<int:id>/season')
def show(id):
    show = queries.get_show(id)
    characters = queries.get_show_characters(id, 3)
    seasons = queries.get_show_seasons(id)

    # format character names
    show['characters_str'] = \
        ', '.join([character['name'] for character in characters])

    # getting trailer id from URL to embed video
    show['trailer_id'] = \
        show['trailer'][show['trailer'].find('=')+1:] if show['trailer'] else ''

    # format runtime
    hours, minutes = divmod(show['runtime'], 60)
    runtime_str = (str(hours)+'h ' if hours else '') + (str(minutes)+'min' if minutes else '')
    show['runtime_str'] = runtime_str

    return render_template('show.html', show=show, seasons=seasons)

# list all show seasons
@app.route('/show/<int:show_id>/season', methods=["POST"])
def add_season(show_id):
    if request.is_json:
        data = request.get_json()
        print(data)
        season_id = data.get('season_id')
        season_number = data.get('season_number')
        season_title = data.get('season_title')
        season_overview = data.get('season_overview')

        add_status = queries.add_season(show_id, season_id, season_number, season_title, season_overview);
        if add_status:
            return jsonify(status='success')
        else:
            return jsonify(status='error')

# LOGIN AND REGISTERING ####################################
import bcrypt
from os import urandom
from flask import session

app.secret_key = urandom(5) # for session
SESSION_KEY = "login"
gensalt_size = 10


@app.route('/login', methods=["GET"])
def login_get():
    pass

@app.route('/login', methods=["POST"])
def login_post():
    if request.is_json:
        data = request.get_json()
        password = data.get('password')
        username = data.get('username')

        user_data = queries.get_user(username)
        if username == user_data.get('username'):
            print(password, password.encode('utf-8'))
            print(user_data.get('password'), user_data.get('password').encode('utf-8'))
            if bcrypt.checkpw(password.encode('utf-8'), user_data.get('password').encode('utf-8')):
                session[SESSION_KEY] = username
                return jsonify(status='success')
            return jsonify(status='error')
        else:
            return jsonify(status='error')


@app.route('/register', methods=["GET"])
def register_get():
    pass

@app.route('/register', methods=["POST"])
def register_post():
    if request.is_json:
        data = request.get_json()
        password = data.get('password')
        username = data.get('username')
        hashpassword  = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(gensalt_size))

        insert_status = queries.insert_new_user(username, hashpassword.decode('utf-8'))
        msg = 'success' if insert_status else 'error'
        return jsonify(status=msg)



###################################################################



# SHOWING EPISODES OF SHOW ########################################

@app.route('/show/<int:show_id>/<int:season_nr>', methods=["GET"])
def get_season_episodes(show_id, season_nr):
    show = queries.get_show(show_id)
    season = queries.get_season(show_id, season_nr)
    episodes = queries.get_season_episodes(show_id, season_nr)

    return render_template('season.html', show=show, season=season, episodes=episodes)


# new route to one show
@app.route('/show/<int:show_id>/<int:season_nr>/<int:episode_nr>', methods=["GET"])
def get_episode(show_id, season_nr, episode_nr):
    show = queries.get_show(show_id)
    season = queries.get_season(show_id, season_nr)
    episode = queries.get_episode(show_id, season_nr, episode_nr)

    return render_template('episode.html', show=show, season=season, episode=episode)

###################################################################

# EDITING AND DELETE EPISODE ######################################
@app.route('/episode', methods=['DELETE'])
def delete_episode():
    if request.is_json:
        data = request.get_json()
        show_id = int(data.get('show_id'))
        season_nr = int(data.get('season_nr'))
        episode_nr = int(data.get('episode_nr'))

        delete_status = queries.delete_episode(show_id,season_nr,episode_nr)
        if delete_status:
            return jsonify(status='success')
        else:
            return jsonify(status='error')

@app.route('/episode', methods=['PATCH'])
def update_episode():
    if request.is_json:
        data = request.get_json()
        show_id = int(data.get('show_id'))
        season_nr = int(data.get('season_nr'))
        episode_nr = int(data.get('episode_nr'))
        new_episode_title = data.get('new_title')
        print(show_id, season_nr, episode_nr, new_episode_title)
        update_status = queries.update_episode(show_id, season_nr, episode_nr, new_episode_title)
        if update_status:
            return jsonify(status='success')
        else:
            return jsonify(status='error')


###################################################################

# ADDING NEW EPISODE ##############################################

@app.route('/episode', methods=['POST'])
def add_episode():
    if request.is_json:
        data = request.get_json()
        show_id = int(data.get('show_id'))
        season_nr = int(data.get('season_nr'))
        episode_nr = int(data.get('episode_nr'))
        episode_title = data.get('title')
        print(data)
        add_status = queries.add_episode(show_id, season_nr, episode_nr, episode_title)
        if add_status:
            return jsonify(status='success')
        else:
            return jsonify(status='error')
##################################################################

# SEARCHING FOR SHOW ##############################################
@app.route('/search', methods=['POST'])
def search():
    search_phrase = request.form.get("search")
    found_show = queries.search_for_title(search_phrase)
    return render_template('search.html', shows=found_show, search_phrase=search_phrase)

##################################################################


# new route to one show
@app.route('/actors/<int:show_id>', methods=['GET'])
def api_actors(show_id):
    actors = queries.get_actors(show_id)
    return jsonify(actors)

##################################################################


@app.route('/shows3season', methods=['GET'])
def shows3season():
    shows = queries.shows3season();
    return render_template("shows3season.html", shows=shows)


@app.route('/actorofaday', methods=['GET', 'POST'])
def actor_of_a_day():
    actors = queries.get_all_actors()
    random_actor = random.choice(actors)
    return jsonify(random_actor)

# editing actor's name
@app.route('/shows/<int:show_id>/actors', methods=['GET'])
def get_actors(show_id):
    show = queries.get_show(show_id)
    actors = queries.get_actors(show_id)
    return render_template('actors.html', show=show, actors=actors)

@app.route('/actor/<int:actor_id>', methods=['POST'])
def edit_actor(actor_id):
    new_name = request.form.get('actor_name')
    queries.update_actor_name(actor_id, new_name)
    return redirect(url_for("get_actor", actor_id=actor_id))

@app.route('/actor/<int:actor_id>', methods=['GET'])
def get_actor(actor_id):
    actor = queries.get_actor(actor_id)
    return render_template('actor.html', actor=actor)




def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
