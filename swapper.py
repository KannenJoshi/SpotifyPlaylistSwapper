import spotipy


# TEMP
playlists = {
    "tense1": "https://open.spotify.com/playlist/2idQqZl9rw63dcwdOrE4bL?si=4de1cf3b5be84e32",
    "svavk4": "https://open.spotify.com/playlist/4G64d75bneOiUhacI7Z1YE?si=b6bf7350453646e3&pt=704e51cd2b3043416551f4063b872bb1"
}


def get_context_uri(name):
    return f'spotify:album:{playlists[name][34:].split("?")[0]}'


def swap_to(sp, context_uri=None, name=None):
    print(context_uri)
    if context_uri is not None:
        sp.start_playback(context_uri=context_uri)
    elif name is not None:
        sp.start_playback(context_uri=get_context_uri(name))
    else:
        raise Exception("Enter a context_uri or name")
