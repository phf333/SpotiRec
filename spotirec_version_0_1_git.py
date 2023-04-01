
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np

########################## spotify

SPOTIPY_CLIENT_ID=''
SPOTIPY_CLIENT_SECRET=''


auth_manager = SpotifyClientCredentials(SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

def seleciona_playlist():
    playlist_link=input("Cole aqui o link de uma playlist do spotify para ser a base de dados: ")
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]

    return playlist_URI


def organiza_base_de_dados(playlist_URI):
    #array com as musicas em vetores
    music_playlist={}

    for track in sp.playlist_tracks(playlist_URI)["items"]:

        #URI
        track_uri = track["track"]["uri"]

        #Audio Features
        music=sp.audio_features(track_uri)[0]
        musicx=sp.audio_analysis(track_uri)
        music_array=np.array=[music['danceability'],
        music['energy'],
        music['key'],
        music['loudness'],
        music['mode'],
        music['speechiness'],
        music['acousticness'],
        music['instrumentalness'],
        music['liveness'],
        music['valence'],
        musicx["track"][ "num_samples" ],
        musicx["track"][ "duration" ],
        musicx["track"][ "offset_seconds" ],
        musicx["track"][ "window_seconds" ],
        musicx["track"][ "analysis_sample_rate" ],
        musicx["track"][ "analysis_channels" ],
        musicx["track"][ "end_of_fade_in" ],
        musicx["track"][ "start_of_fade_out" ],
        musicx["track"][ "loudness" ],
        musicx["track"][ "tempo" ],
        musicx["track"][ "tempo_confidence" ],
        musicx["track"][ "time_signature" ],
        musicx["track"][ "time_signature_confidence" ],
        musicx["track"][ "key" ],
        musicx["track"][ "key_confidence" ],
        musicx["track"][ "mode" ],
        musicx["track"][ "mode_confidence" ],
        musicx["track"][ "code_version" ],
        musicx["track"][ "synch_version" ],
        musicx["track"][ "rhythm_version" ]
        ]

        #Add URI and Music_array in music_playlist
        music_playlist[track_uri]=music_array

    return music_playlist


###################### linear algebra

def cos(v,w):
    int_prod= np.inner(v,w)
    cos=int_prod/(np.linalg.norm(v)*np.linalg.norm(w))
    return cos

def compare_songs_with_playlist(song,playlist):
    cosseno=0
    similar_song=[]
    for i in playlist:
        #print(similar_song)
        result=cos(song,playlist[i])
        if result==0 or result<0:
            continue
        else:
            if result > cosseno:
                cosseno=result
                similar_song=[i,playlist[i]]
            else:
                cosseno=cosseno
    
    return sp.track(similar_song[0]).get("name"),sp.track(similar_song[0])["artists"][0]["name"],cosseno
        


def main():
    playlist=seleciona_playlist()
    music_array=organiza_base_de_dados(playlist)

    while True:
        # Pesquisar por uma música
        query = input("Qual o nome da musica?")
        result = sp.search(query, limit=5, type='track')
        
        # Organizar Musicas e Apresentar para escolha

        for i in range(5):
            track = result['tracks']['items'][i]
            print("Musica(",i,")","Nome da música:", track['name'],"  ", "Artista:", track['artists'][0]['name'])

        musica_escolhida=int(input("Qual dessas opçoes é sua música?"))

        # Obter informações da música

        track = result['tracks']['items'][musica_escolhida]

        print("Nome da música:", track['name'])
        print("Artista:", track['artists'][0]['name'])
        #print("Álbum:", track['album']['name'])
        #print("Link da música:", track['external_urls']['spotify'])

        
        musica_selecionada=track['external_urls']['spotify']
        print("\n")

        music=sp.audio_features(musica_selecionada)[0]
        musicx=sp.audio_analysis(musica_selecionada)

        musica1_array=np.array=[music['danceability'],
        music['energy'],
        music['key'],
        music['loudness'],
        music['mode'],
        music['speechiness'],
        music['acousticness'],
        music['instrumentalness'],
        music['liveness'],
        music['valence'],
        musicx["track"][ "num_samples" ],
        musicx["track"][ "duration" ],
        musicx["track"][ "offset_seconds" ],
        musicx["track"][ "window_seconds" ],
        musicx["track"][ "analysis_sample_rate" ],
        musicx["track"][ "analysis_channels" ],
        musicx["track"][ "end_of_fade_in" ],
        musicx["track"][ "start_of_fade_out" ],
        musicx["track"][ "loudness" ],
        musicx["track"][ "tempo" ],
        musicx["track"][ "tempo_confidence" ],
        musicx["track"][ "time_signature" ],
        musicx["track"][ "time_signature_confidence" ],
        musicx["track"][ "key" ],
        musicx["track"][ "key_confidence" ],
        musicx["track"][ "mode" ],
        musicx["track"][ "mode_confidence" ],
        musicx["track"][ "code_version" ],
        musicx["track"][ "synch_version" ],
        musicx["track"][ "rhythm_version" ]]

        print("Voce Escolheu a música: ",sp.track(musica_selecionada).get("name"),sp.track(musica_selecionada)["artists"][0]["name"])
        print("\n")
        print("A musica que mais aproxima você de Paulo Henrique é.....")
        print("\n")
        print((compare_songs_with_playlist(musica1_array,music_array)))

    return 0


main()


