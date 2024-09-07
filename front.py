import tkinter as tk
from tkinter import messagebox, filedialog


import pygame
import os
import random

from back import MusicPlayerBackend

class MusicPlayerApp:
    def __init__(self, root):
        self.back= MusicPlayerBackend()
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("800x600")
        self.root.configure(bg='#282828')
        self.current_song_index = None
        self.is_shuffled = False
        self.create_home_page()
        pygame.mixer.init()

    def create_home_page(self):
        self.clear_frame()
        tk.Label(self.root, text="Welcome to Music Player", font=("Helvetica", 20), bg='#282828', fg='white').pack(pady=20)
        tk.Button(self.root, text="Login", command=self.show_login_page, bg='#1DB954', fg='white', font=("Helvetica", 14)).pack(pady=10)
        tk.Button(self.root, text="Signup", command=self.show_signup_page, bg='#1DB954', fg='white', font=("Helvetica", 14)).pack(pady=10)

    def show_login_page(self):
        self.clear_frame()
        tk.Label(self.root, text="Login", font=("Helvetica", 20), bg='#282828', fg='white').pack(pady=20)
        tk.Label(self.root, text="Username", bg='#282828', fg='white').pack()
        self.login_username_entry = tk.Entry(self.root)
        self.login_username_entry.pack()
        tk.Label(self.root, text="Password", bg='#282828', fg='white').pack()
        self.login_password_entry = tk.Entry(self.root, show='*')
        self.login_password_entry.pack()
        tk.Button(self.root, text="Login", command=self.login, bg='#1DB954', fg='white').pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_home_page, bg='#1DB954', fg='white').pack(pady=10)

    def show_signup_page(self):
        self.clear_frame()
        tk.Label(self.root, text="Signup", font=("Helvetica", 20), bg='#282828', fg='white').pack(pady=20)
        tk.Label(self.root, text="Username", bg='#282828', fg='white').pack()
        self.signup_username_entry = tk.Entry(self.root)
        self.signup_username_entry.pack()
        tk.Label(self.root, text="Password", bg='#282828', fg='white').pack()
        self.signup_password_entry = tk.Entry(self.root, show='*')
        self.signup_password_entry.pack()
        tk.Label(self.root, text="User Type", bg='#282828', fg='white').pack()
        self.signup_type_var = tk.StringVar(value='user')
        tk.Radiobutton(self.root, text="User", variable=self.signup_type_var, value='user', bg='#282828', fg='white').pack()
        tk.Radiobutton(self.root, text="Artist", variable=self.signup_type_var, value='artist', bg='#282828', fg='white').pack()
        tk.Button(self.root, text="Signup", command=self.signup, bg='#1DB954', fg='white').pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_home_page, bg='#1DB954', fg='white').pack(pady=10)

    def login(self):
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()
        user = self.back.login(username, password)
        if user:
            self.user_id, self.user_type = user
            if self.user_type == 'artist':
                self.show_artist_page()
            else:
                self.show_user_page()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    def signup(self):
        username = self.signup_username_entry.get()
        password = self.signup_password_entry.get()
        user_type = self.signup_type_var.get()
        if self.back.signup(username, password, user_type):
            messagebox.showinfo("Signup Success", "Signup successful, please login")
            self.show_login_page()
        else:
            messagebox.showerror("Signup Failed", "Username already exists")

    def show_artist_page(self):
        self.clear_frame()
        tk.Label(self.root, text="Artist Dashboard", font=("Helvetica", 20), bg='#282828', fg='white').pack(pady=20)
        tk.Button(self.root, text="Upload Song", command=self.show_upload_song_page, bg='#1DB954', fg='white').pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.logout, bg='#1DB954', fg='white').pack(pady=10)

    def show_user_page(self):
        self.clear_frame()
        tk.Label(self.root, text="User Dashboard", font=("Helvetica", 20), bg='#282828', fg='white').pack(pady=20)
        
        song_frame = tk.Frame(self.root, bg='#282828')
        song_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        self.song_listbox = tk.Listbox(song_frame, bg='#333333', fg='white', selectbackground='#1DB954')
        self.song_listbox.pack(pady=10)
        
        songs = self.back.get_songs()
        for song in songs:
            self.song_listbox.insert(tk.END, song[1])
        
        self.song_listbox.bind('<<ListboxSelect>>', self.show_song_details)
        
        button_frame = tk.Frame(song_frame, bg='#282828')
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Play", command=self.play_song, bg='#1DB954', fg='white').pack(pady=5)
        tk.Button(button_frame, text="Add to Playlist", command=self.add_to_playlist, bg='#1DB954', fg='white').pack(pady=5)
        tk.Button(button_frame, text="View Playlist", command=self.show_playlist, bg='#1DB954', fg='white').pack(pady=5)
        tk.Button(button_frame, text="Back", command=self.create_home_page, bg='#1DB954', fg='white').pack(pady=5)
        tk.Button(button_frame, text="Logout", command=self.logout, bg='#1DB954', fg='white').pack(pady=5)
        
        details_frame = tk.Frame(self.root, bg='#282828')
        details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(details_frame, text="Song Details", font=("Helvetica", 20), bg='#282828', fg='white').pack(pady=10)
        self.song_details_label = tk.Label(details_frame, text="", font=("Helvetica", 14), bg='#282828', fg='white', justify=tk.LEFT)
        self.song_details_label.pack(pady=10, anchor=tk.NW)
        
        self.create_music_controls(details_frame)

    def show_upload_song_page(self):
        self.clear_frame()
        tk.Label(self.root, text="Upload Song", font=("Helvetica", 20), bg='#282828', fg='white').pack(pady=20)
        tk.Label(self.root, text="Title", bg='#282828', fg='white').pack()
        self.song_title_entry = tk.Entry(self.root)
        self.song_title_entry.pack()
        tk.Label(self.root, text="Description", bg='#282828', fg='white').pack()
        self.song_description_entry = tk.Entry(self.root)
        self.song_description_entry.pack()
        tk.Label(self.root, text="Lyrics", bg='#282828', fg='white').pack()
        self.song_lyrics_entry = tk.Entry(self.root)
        self.song_lyrics_entry.pack()
        tk.Label(self.root, text="File", bg='#282828', fg='white').pack()
        self.song_file_path = tk.Entry(self.root)
        self.song_file_path.pack()
        tk.Button(self.root, text="Browse", command=self.browse_file, bg='#1DB954', fg='white').pack(pady=10)
        tk.Button(self.root, text="Upload", command=self.upload_song, bg='#1DB954', fg='white').pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_artist_page, bg='#1DB954', fg='white').pack(pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.song_file_path.delete(0, tk.END)
            self.song_file_path.insert(0, file_path)

    def upload_song(self):
        title = self.song_title_entry.get()
        description = self.song_description_entry.get()
        lyrics = self.song_lyrics_entry.get()
        filepath = self.song_file_path.get()
        self.back.upload_song(self.user_id, title, description, lyrics, filepath)
        messagebox.showinfo("Upload Success", "Song uploaded successfully")
        self.show_artist_page()

    def show_playlist(self):
        self.clear_frame()
        tk.Label(self.root, text="Your Playlist", font=("Helvetica", 20), bg='#282828', fg='white').pack(pady=20)
        self.playlist_listbox = tk.Listbox(self.root, bg='#333333', fg='white', selectbackground='#1DB954')
        self.playlist_listbox.pack(pady=10)
        songs = self.back.get_playlist_songs(self.user_id)
        for song in songs:
            self.playlist_listbox.insert(tk.END, song[1])
        tk.Button(self.root, text="Back", command=self.show_user_page, bg='#1DB954', fg='white').pack(pady=10)

    def show_song_details(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            self.current_song_index = index
            song = self.back.get_songs()[index]
            details = f"Title: {song[1]}\n\nDescription: {song[2]}\n\nLyrics:\n{song[3]}"
            self.song_details_label.config(text=details)

    def create_music_controls(self, frame):
        control_frame = tk.Frame(frame, bg='#282828')
        control_frame.pack(pady=10)
        tk.Button(control_frame, text="Play", command=self.play_song, bg='#1DB954', fg='white').pack(side=tk.LEFT, padx=10)
        tk.Button(control_frame, text="Pause", command=self.pause_song, bg='#1DB954', fg='white').pack(side=tk.LEFT, padx=10)
        tk.Button(control_frame, text="Stop", command=self.stop_song, bg='#1DB954', fg='white').pack(side=tk.LEFT, padx=10)
        tk.Button(control_frame, text="Next", command=self.next_song, bg='#1DB954', fg='white').pack(side=tk.LEFT, padx=10)

        tk.Label(control_frame, text="Volume", bg='#282828', fg='white').pack(side=tk.LEFT, padx=10)
        self.volume_slider = tk.Scale(control_frame, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, bg='#282828', fg='white', command=self.change_volume)
        self.volume_slider.set(0.5)
        self.volume_slider.pack(side=tk.LEFT, padx=10)

    def play_song(self):
        if self.current_song_index is not None:
            song = self.back.get_songs()[self.current_song_index]
            pygame.mixer.music.load(song[4])
            pygame.mixer.music.play()

    def pause_song(self):
        pygame.mixer.music.pause()

    def stop_song(self):
        pygame.mixer.music.stop()

    def next_song(self):
        songs = self.back.get_songs()
        if self.current_song_index is not None:
            next_index = (self.current_song_index + 1) % len(songs)
            self.current_song_index = next_index
            song = songs[next_index]
            pygame.mixer.music.load(song[4])
            pygame.mixer.music.play()
            details = f"Title: {song[1]}\n\nDescription: {song[2]}\n\nLyrics:\n{song[3]}"
            self.song_details_label.config(text=details)

    def change_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume))

    def add_to_playlist(self):
        if self.current_song_index is not None:
            song = self.back.get_songs()[self.current_song_index]
            self.back.add_to_playlist(self.user_id, song[0])
            messagebox.showinfo("Playlist", "Song added to playlist")

    def logout(self):
        self.user_id = None
        self.user_type = None
        self.create_home_page()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayerApp(root)
    root.mainloop()
