from music21 import *

# Get and parse the xml file
song = converter.parse('C:/Users/Matthieu/Documents/MuseScore2/Scores/Test.xml')

# Assign each chord symbol its proper duration
harmony.realizeChordSymbolDurations(song)

# Transpose to C
keySig = song.flat.getElementsByClass(key.KeySignature)[0]
dist = interval.Interval(keySig.asKey().tonic, pitch.Pitch('C'))
transposed = song.transpose(dist)

# Stores note/chord pairs
tuples = []

# Get the pairs from the score (TODO...)
for cs in transposed.flat.getElementsByClass(harmony.ChordSymbol):
    for n in transposed.flat.getElementsByClass(note.Note):
        if n.offset >= cs.offset and n.offset < (cs.offset + cs.duration.quarterLength):
            pair = (n, cs)
            tuples.append(pair)
            
print(tuples) # Feed tuples to HMM