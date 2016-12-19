from music21 import *
import pickle

# Load the list of song data else create a new one
try:
    songList = pickle.load(open("song_data.pickle", "rb"))
except IOError:
    songList = []

# Get and parse the xml file
currentSong = converter.parse("TOSCA-Melody.xml")

# Assign each chord symbol its proper duration
harmony.realizeChordSymbolDurations(currentSong)

# Get first key signature and transpose to C
keySig = currentSong.flat.getElementsByClass(key.KeySignature)[0]
dist = interval.Interval(keySig.asKey().tonic, pitch.Pitch('C'))
transposed = currentSong.transpose(dist)

# Stores note/chord pairs
noteTuples = []

# Get the pairs from the score
for cs in transposed.flat.getElementsByClass(harmony.ChordSymbol):
    for n in transposed.flat.getElementsByClass(note.Note):
        if n.offset >= cs.offset and n.offset < (cs.offset + cs.duration.quarterLength):
            if n.pitch.accidental and n.pitch.accidental.name == 'flat': # Convert flats to sharps for model
                n.pitch.getEnharmonic(inPlace = True)
                
            if cs.root().accidental and cs.root().accidental.name == 'flat':
                cs.root().getEnharmonic(inPlace = True)
            
            pair = (n.name, cs.figure)
            noteTuples.append(pair)

# Append current song data to song list and pickle          
songList.append(noteTuples)
pickle.dump(songList, open("song_data.pickle", "wb"))

print(songList)