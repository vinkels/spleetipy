from spleeter.separator import Separator
from spleeter.audio.adapter import AudioAdapter
# default_adapter = AudioAdapter.default()

def remove_instrument(song_path, filter_instrument=None):
    
    instruments = ["vocals", "bass","drums", "other"]
    others = [i for i in instruments if i != filter_instrument]
    # Using embedded configuration.
    separator = Separator('spleeter:4stems')

    audio_adapter = AudioAdapter.default()
    sample_rate = 44100
    waveform, _ = audio_adapter.load(song_path, sample_rate=sample_rate)
    prediction = separator.separate(waveform)

    # Now add up all that is not drums
    out = prediction[others[0]]
    for key in others[1:]:
        out += prediction[key]
    song_name = song_path.split('/')[-1].replace('.mp3','')
    new_name = f"stemmed/{song_name}_without_{filter_instrument}.mp3"
    audio_adapter.save(new_name, out, separator._sample_rate, "mp3", "128k")
    return new_name
    