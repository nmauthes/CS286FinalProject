from music21 import *
import yahmm

# import model
file = open('model.txt', 'r')
model = yahmm.Model.read(file)
file.close()

# Get note sequence from music xml
s = converter.parse("input.xml")

# Get first key signature and transpose to C
keySig = s.flat.getElementsByClass(key.KeySignature)[0]
dist = interval.Interval(keySig.asKey().tonic, pitch.Pitch('C'))
transposed = s.transpose(dist)

# Get note names as strings and put in list
sequence = []
for n in s.flat.getElementsByClass(note.Note):
    sequence.append(n.name)

# use imported model to generate chords based on roboccini output
logp, path = model.viterbi( sequence )
if path is not None:
    # Build chord symbol objs and transpose to original key
    symbols = []
    for state in path:
        newSymbol = harmony.ChordSymbol(state[1].name)
        newSymbol.transpose(dist.reverse(), inPlace = True)
        symbols.append(newSymbol)
    
    # Add the chord symbols to the start of each measure
    for index, cs in enumerate(symbols):
        cs.priority = -1
        s.parts[0].measure(index + 1).insert(0, cs)
        
    # Write new score to file
    s.write("musicxml", "output.xml")
else:
    print('No path found')