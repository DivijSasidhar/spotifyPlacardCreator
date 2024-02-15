import spotipy
from time import sleep
import requests
from msvcrt import getch
from spotipy.oauth2 import SpotifyClientCredentials

print("Creator: Divij Sasidhar & Arnav Sahni")
print("NOT FOR REPRODUCTION WITHOUT AUTHORIZATION")
print('CONTACT divijsasi@gmail.com FOR MORE INFORMATION\n')


class Track:
    def __init__(self, name, uri, artist_name, duration, album_cover):
        self.name = name
        self.song_uri = uri
        self.artist_name = artist_name
        self.duration = duration
        self.album_cover = album_cover

    def __str__(self):
        return f"Track name: {self.name}\n" \
               f"URI: {self.song_uri}\n" \
               f"Artist name: {self.artist_name}\n" \
               f"Duration: {self.duration}"


with open('config.txt', 'r') as f:
    client_id = f.readline().split(' ')[1][:-1]
    client_secret = f.readline().split(' ')[1]

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id, client_secret))


name = (input("Enter Song Title: "))
results = spotify.search(q=name, type='track')
results = results['tracks']['items']
tracks = []
i = 0
for track_number in results:
    print(str(i) + " | " + track_number['name'] + ' | ' + track_number['album']['name'], end=" | ")
    artists = []
    for artist in track_number['album']['artists']:
        artists.append(artist['name'])
        print(artist['name'], end=", ")
    album_cover = track_number['album']['images'][0]['url']
    print(album_cover)
    tracks.append(Track(
        track_number['name'],
        track_number['uri'][0:len(track_number['uri'])],
        artists,
        track_number['duration_ms'],
        album_cover)
    )
    i += 1

print("\nEnter the number of the track you'd like to print: ", end="")
track = tracks[int(getch())]


print(f"\nPress [Enter] to confirm printing of {track.name} by", track.artist_name[0])
if getch() != b'\r':
    print("Quitting program...")
    sleep(3)
    exit()

print("Saving files...")

# spotify code
url = f"https://scannables.scdn.co/uri/plain/png/000000/white/640/{track.song_uri}"
data = requests.get(url).content
with open(f'{track.name}_spotify_code.png', 'wb') as f:
    f.write(data)

# album cover
data = requests.get(track.album_cover).content
with open(f'{track.name}_album_cover.png', 'wb') as f:
    f.write(data)
