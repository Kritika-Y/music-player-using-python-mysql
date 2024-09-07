import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

class MusicPlayerBackend:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='692028@Kt',
            database='music_play'
        )
        self.cursor = self.conn.cursor()

    def signup(self, username, password, user_type):
        hashed_password = generate_password_hash(password)
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password, type) VALUES (%s, %s, %s)",
                (username, hashed_password, user_type)
            )
            self.conn.commit()
            return True
        except mysql.connector.IntegrityError:
            return False

    def login(self, username, password):
        self.cursor.execute("SELECT id, password, type FROM users WHERE username = %s", (username,))
        user = self.cursor.fetchone()
        if user and check_password_hash(user[1], password):
            return user[0], user[2]
        return None

    def upload_song(self, artist_id, title, description, lyrics, filepath):
        self.cursor.execute(
            "INSERT INTO songs (artist_id, title, description, lyrics, filepath) VALUES (%s, %s, %s, %s, %s)",
            (artist_id, title, description, lyrics, filepath)
        )
        self.conn.commit()

    def get_songs(self):
        self.cursor.execute("SELECT id, title, description, lyrics, filepath FROM songs")
        return self.cursor.fetchall()

    def add_to_playlist(self, user_id, song_id):
        self.cursor.execute(
            "INSERT INTO playlists (user_id, song_id) VALUES (%s, %s)",
            (user_id, song_id)
        )
        self.conn.commit()

   
    def get_playlist_songs(self, user_id):
        self.cursor.execute("""
            SELECT songs.id, songs.title, songs.description, songs.lyrics, songs.filepath
            FROM playlists
            JOIN songs ON playlists.song_id = songs.id
            WHERE playlists.user_id = %s
        """, (user_id,))
        return self.cursor.fetchall()