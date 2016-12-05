import yahmm

# import model
file = open('model.txt', 'r')
model = yahmm.Model.read(file)

# use imported model to generate chords based on roboccini output
sequence = ['C', 'G']
logp, path = model.viterbi( sequence )
print(path)
for state in path:
    print(state[1].name)