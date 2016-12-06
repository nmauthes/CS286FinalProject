import yahmm

# import model
file = open('model.txt', 'r')
model = yahmm.Model.read(file)
file.close()

# use imported model to generate chords based on roboccini output
sequence = ['C', 'A', 'F', 'D' ]
logp, path = model.viterbi( sequence )
if path is not None:
    for state in path:
        print(state[1].name)
else:
    print('No path found')