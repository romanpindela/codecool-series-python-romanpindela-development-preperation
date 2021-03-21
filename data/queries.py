from data import data_manager
from psycopg2 import sql


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')


def get_show_count():
    return data_manager.execute_select('SELECT count(*) FROM shows;')


def get_shows_limited(order_by="rating", order="DESC", limit=0, offset=0):
    return data_manager.execute_select(
        sql.SQL("""
            SELECT
                shows.id,
                shows.title,
                shows.year,
                shows.runtime,
                to_char(shows.rating::float, '999.9') AS rating_string,
                string_agg(genres.name, ', ' ORDER BY genres.name) AS genres_list,
                shows.trailer,
                shows.homepage
            FROM shows
                JOIN show_genres ON shows.id = show_genres.show_id
                JOIN genres ON show_genres.genre_id = genres.id
            GROUP BY shows.id
            ORDER BY
                CASE WHEN %(order)s = 'ASC' THEN {order_by} END ASC,
                CASE WHEN %(order)s = 'DESC' THEN {order_by} END DESC
            LIMIT %(limit)s
            OFFSET %(offset)s;
        """
        ).format(order_by=sql.Identifier(order_by)),
        {"order": order, "limit": limit, "offset": offset}
   )


def get_show(id):
    return data_manager.execute_select("""
        SELECT
            shows.id,
            shows.title,
            shows.year,
            shows.runtime,
            to_char(shows.rating::float, '999.9') AS rating_string,
            string_agg(genres.name, ', ' ORDER BY genres.name) AS genres_list,
            shows.trailer,
            shows.homepage,
            shows.overview
        FROM shows
            JOIN show_genres ON shows.id = show_genres.show_id
            JOIN genres ON show_genres.genre_id = genres.id
        WHERE shows.id = %(id)s
        GROUP BY shows.id;
    """, {"id": id}, False)


def get_show_characters(id, limit=3):
    return data_manager.execute_select("""
        SELECT sc.id, character_name, name, birthday, death, biography
        FROM actors a
        JOIN show_characters sc on a.id = sc.actor_id
        WHERE show_id = %(id)s
        ORDER BY id
        LIMIT %(limit)s;
    """, {"id": id, "limit": limit})


def get_show_seasons(id):
    return data_manager.execute_select("""
        SELECT
            season_number,
            seasons.title,
            seasons.overview
        FROM shows
        JOIN seasons ON shows.id = seasons.show_id
        WHERE shows.id = %(id)s;
    """, {"id": id})



# LOGIN AND REGISTERING ####################################
def insert_new_user(username, hashpassword):
    try:
        data_manager.execute_dml_statement("""
            INSERT INTO users(username, password)
            VALUES (%(username)s, %(hashpassword)s );
        """, {'username': username, 'hashpassword': hashpassword})
        return True
    except:
        return False

def get_user(username):
    return data_manager.execute_select("""
        SELECT username, password
        FROM users
        WHERE username = %(username)s;
    """, {'username': username}, False)
###################################################################

# SHOWING EPISODES OF SHOW ########################################

def get_season(show_id, season_nr):
    return data_manager.execute_select("""
        SELECT seasons.*
        FROM seasons
        WHERE seasons.show_id = %(show_id)s
            AND seasons.season_number = %(season_nr)s
    """, {'show_id': show_id, 'season_nr': season_nr}, False)


def get_season_episodes(show_id, season_nr):
    return data_manager.execute_select("""
        SELECT episodes.*
        FROM seasons 
        INNER JOIN shows on shows.id = seasons.show_id
        INNER JOIN episodes on episodes.season_id = seasons.id
        WHERE shows.id = %(show_id)s 
            AND seasons.season_number = %(season_nr)s
        ORDER BY episodes.episode_number;
        """, { 'show_id':show_id, 'season_nr': season_nr }, True)

def get_episode(show_id, season_nr, episode_nr):
    return data_manager.execute_select("""
        SELECT episodes.*
        FROM seasons 
        INNER JOIN shows on shows.id = seasons.show_id
        INNER JOIN episodes on episodes.season_id = seasons.id
        WHERE shows.id = %(show_id)s 
            AND seasons.season_number = %(season_nr)s
            AND episodes.episode_number = %(episode_nr)s;
        """, { 'show_id':show_id, 'season_nr': season_nr, 'episode_nr': episode_nr }, False)




###################################################################



# EDITING EPISODE TITLE AND DELETING IT  ##########################
def update_episode(show_id, season_nr, episode_nr, new_title):
    try:
        data_manager.execute_dml_statement("""
            UPDATE episodes
            SET title = %(new_title)s
            FROM seasons
            WHERE seasons.show_id = %(show_id)s
            AND seasons.season_number = %(season_nr)s
            AND episodes.episode_number = %(episode_nr)s
            AND seasons.id = episodes.season_id
        """, {'show_id':show_id, 'season_nr':season_nr , 'episode_nr':episode_nr, 'new_title':new_title})
        return True
    except:
        return False

def delete_episode(show_id, season_nr, episode_nr):
    try:
        data_manager.execute_dml_statement("""
            DELETE
            FROM episodes
            USING seasons
            WHERE seasons.show_id = %(show_id)s
            AND seasons.season_number = %(season_nr)s
            AND episodes.episode_number = %(episode_nr)s
            AND seasons.id = episodes.season_id
        """, {'show_id':show_id, 'season_nr':season_nr, 'episode_nr':episode_nr})
        return True
    except:
        return False

def add_episode(show_id, season_nr, episode_nr, episode_title):
    try:
        season_id_dict = data_manager.execute_select("""
            select seasons.id
            from seasons
            where seasons.show_id = %(show_id)s
            and seasons.season_number = %(season_nr)s
        """, {'show_id':show_id, 'season_nr': season_nr}, False)
        season_id = int(season_id_dict['id'])
        print(season_id, season_nr)
        max_taken_episode_id_dict = data_manager.execute_select("""
            SELECT MAX(id)
            FROM episodes 
        """, fetchall=False)
        max_taken_episode_id = int(max_taken_episode_id_dict['max'])
        episode_id = max_taken_episode_id + 1;
        print(max_taken_episode_id, episode_nr)
        data_manager.execute_dml_statement("""
            INSERT INTO episodes (id, title, episode_number, season_id)
            VALUES ( %(episode_id)s, %(episode_title)s, %(episode_nr)s, %(season_id)s )
        """, {'show_id':show_id, 'season_id':season_id, 'episode_nr':episode_nr, 'episode_title': episode_title, 'episode_id':episode_id})
        return True
    except:
        return False

###################################################################


# SEARCHING FOR TITLE OF SHOW  ########################################
def search_for_title(phrase):
    return data_manager.execute_select(f""" 
        SELECT shows.id, shows.title
        FROM shows
        WHERE shows.title ILIKE '%{phrase}%'
    """, fetchall=True)

###################################################################

# editing actor's name
def get_actors(show_id):
    return data_manager.execute_select(""" 
        SELECT show_characters.*, actors.name, actors.id as actor_id
        FROM show_characters
        INNER JOIN actors on show_characters.actor_id = actors.id
        WHERE show_id = 1399
        ORDER BY actors.name
    """,{'show_id':show_id}, fetchall=True)

def get_all_actors():
    return data_manager.execute_select(""" 
        SELECT * FROM actors
    """)

def get_actor(actor_id):
    return data_manager.execute_select(""" 
        SELECT actors.*
        FROM actors
        WHERE actors.id = %(actor_id)s
    """, {'actor_id': actor_id}, fetchall=False)

def update_actor_name(actor_id, new_name):
    return data_manager.execute_dml_statement(""" 
        UPDATE actors
        SET name = %(new_name)s
        WHERE actors.id = %(actor_id)s
    """, {'actor_id': actor_id, 'new_name': new_name})


# list all show seasons
def add_season(show_id, season_id, season_number, season_title, season_overview):
    try:
        data_manager.execute_dml_statement(""" 
        INSERT INTO seasons(id, season_number, title, overview, show_id) 
        VALUES (%(season_id)s, %(season_number)s, %(season_title)s, %(season_overview)s, %(show_id)s)
        """, {'show_id':show_id, 'season_id':season_id, 'season_number':season_number, 'season_title':season_title, 'season_overview':season_overview })
        return True
    except:
        return False


def shows3season():
    return data_manager.execute_select(""" 
        SELECT shows.title, shows.rating, seasons.overview
        FROM shows
        INNER JOIN seasons on shows.id = seasons.show_id
        WHERE seasons.season_number = 3;
    """)









###################################################################