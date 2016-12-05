from yahmm import *

# for sequence in map( list, ('ACT', 'GGC', 'GAT', 'ACC') ):
#     print sequence
#
#
# rainy = State( DiscreteDistribution({ 'walk': 0.1, 'shop': 0.4, 'clean': 0.5 }), name='Rainy' )
#
# print rainy.name
file = open('model.txt', 'r')
model = Model(name="chord-generator")
model.read(file)


# use imported model to generate chords based on roboccini output

sequence = ['C']
logp, path = model.viterbi( sequence )
print path
# for state in path:
#     print state.name