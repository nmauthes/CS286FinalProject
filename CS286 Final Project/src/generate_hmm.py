import yahmm
import pickle

# all possible notes
notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
# notes = [note.Note("C")]
# chord types: major, minor
chord_types = ['', 'm', 'aug', '+']
# start off with start and end, chords are our hidden states
chords = ['start', 'end']

# used in add_data, initialize to 0 (start)
previous_chord_index = 0

# build out the chords based on chord types
for chord in chord_types:
    for note in notes:
        chords.append(note + chord)

# 2 + 4 * 12 = 50 chords
print("number of chords:" ,len(chords), " and chords: ")
print(chords)

# initialize emission_matrix and transition_matrix to all 0s
emission_matrix = [[0 for x in range(len(notes))] for y in range(len(chords)-2)]
transition_matrix = [[0 for x in range(len(chords))] for y in range(len(chords))]
import pprint
pprint.pprint(emission_matrix)
pprint.pprint(transition_matrix)
# -------------------------------------------------------------------------------


# add training data (tuple)
def add_data(note_chord_pair):
    next_note, next_chord = note_chord_pair
    global previous_chord_index
    note_index = notes.index(next_note)
    chord_index = chords.index(next_chord)
    # increment the two matrices
    emission_matrix[chord_index - 2][note_index] += 1
    transition_matrix[previous_chord_index][chord_index] += 1
    # keep track of current chord
    previous_chord_index = chord_index


# normalize each row in the two matrices
def normalize_matrices():
    for row in range(len(emission_matrix)):
        row_total = 0
        for col in range(len(emission_matrix[row])):
            row_total += emission_matrix[row][col]
        for col in range(len(emission_matrix[row])):
            if row_total is not 0:
                emission_matrix[row][col] /= row_total
    for row in range(len(emission_matrix)):
        row_total = 0
        for col in range(len(transition_matrix[row])):
            row_total += transition_matrix[row][col]
        for col in range(len(transition_matrix[row])):
            if row_total is not 0:
                transition_matrix[row][col] /= row_total


# each song is a list of tuples
# training data is a list of list of tuples (or set of tuple of tuples)
try:
    training_data = pickle.load(open("song_data.pickle", "rb"))
except IOError:
    print('no data loaded, so load dummy data')
    training_data = [[('C', 'C'), ('A', 'Amin')], [('C', 'C'), ('A', 'Amin')]]

for song in training_data:
    for note in song:
        add_data(note)
    # add transition for end of song
    transition_matrix[previous_chord_index][1] += 1
    # reset to beginning of song
    previous_chord_index = 0

# print emission_matrix
normalize_matrices()


def build_distribution(index):
    for i in range(len(emission_matrix[index])):
        dists[index][chords[i+2]]= emission_matrix[index][i]
    # print(dists[index])


# TO DO... build out the distribution dictionary for c major chord
c_distribution, cs_distribution, d_distribution, ds_distribution, e_distribution, f_distribution, fs_distribution, g_distribution, gs_distribution, a_distribution, as_distribution, b_distribution = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
cmin_distribution, csmin_distribution, dmin_distribution, dsmin_distribution, emin_distribution, fmin_distribution, fsmin_distribution, gmin_distribution, gsmin_distribution, amin_distribution, asmin_distribution, bmin_distribution = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
caug_distribution, csaug_distribution, daug_distribution, dsaug_distribution, eaug_distribution, faug_distribution, fsaug_distribution, gaug_distribution, gsaug_distribution, aaug_distribution, asaug_distribution, baug_distribution = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
cdim_distribution, csdim_distribution, ddim_distribution, dsdim_distribution, edim_distribution, fdim_distribution, fsdim_distribution, gdim_distribution, gsdim_distribution, adim_distribution, asdim_distribution, bdim_distribution = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}

dists = [c_distribution, cs_distribution, d_distribution, ds_distribution, e_distribution, f_distribution,
         fs_distribution, g_distribution, gs_distribution, a_distribution, as_distribution, b_distribution,
         cmin_distribution, csmin_distribution, dmin_distribution, dsmin_distribution, emin_distribution,
         fmin_distribution, fsmin_distribution, gmin_distribution, gsmin_distribution, amin_distribution,
         asmin_distribution, bmin_distribution, caug_distribution, csaug_distribution, daug_distribution,
         dsaug_distribution, eaug_distribution, faug_distribution, fsaug_distribution, gaug_distribution,
         gsaug_distribution, aaug_distribution, asaug_distribution, baug_distribution, cdim_distribution,
         csdim_distribution, ddim_distribution, dsdim_distribution, edim_distribution, fdim_distribution,
         fsdim_distribution, gdim_distribution, gsdim_distribution, adim_distribution, asdim_distribution,
         bdim_distribution]

# build distributions from emission matrix
for i in range(len(dists)):
    build_distribution(i)

# create model
model = yahmm.Model(name="chord-generator")
# represents a hidden state
c_state = yahmm.State(yahmm.DiscreteDistribution(dists[0]), name=chords[2])
cs_state = yahmm.State(yahmm.DiscreteDistribution(dists[1]), name=chords[3])
d_state = yahmm.State(yahmm.DiscreteDistribution(dists[2]), name=chords[4])
ds_state = yahmm.State(yahmm.DiscreteDistribution(dists[3]), name=chords[5])
e_state = yahmm.State(yahmm.DiscreteDistribution(dists[4]), name=chords[6])
f_state = yahmm.State(yahmm.DiscreteDistribution(dists[5]), name=chords[7])
fs_state = yahmm.State(yahmm.DiscreteDistribution(dists[6]), name=chords[8])
g_state = yahmm.State(yahmm.DiscreteDistribution(dists[7]), name=chords[9])
gs_state = yahmm.State(yahmm.DiscreteDistribution(dists[8]), name=chords[10])
a_state = yahmm.State(yahmm.DiscreteDistribution(dists[9]), name=chords[11])
as_state = yahmm.State(yahmm.DiscreteDistribution(dists[10]), name=chords[12])
b_state = yahmm.State(yahmm.DiscreteDistribution(dists[11]), name=chords[13])

cmin_state = yahmm.State(yahmm.DiscreteDistribution(dists[12]), name=chords[14])
csmin_state = yahmm.State(yahmm.DiscreteDistribution(dists[13]), name=chords[15])
dmin_state = yahmm.State(yahmm.DiscreteDistribution(dists[14]), name=chords[16])
dsmin_state = yahmm.State(yahmm.DiscreteDistribution(dists[15]), name=chords[17])
emin_state = yahmm.State(yahmm.DiscreteDistribution(dists[16]), name=chords[18])
fmin_state = yahmm.State(yahmm.DiscreteDistribution(dists[17]), name=chords[19])
fsmin_state = yahmm.State(yahmm.DiscreteDistribution(dists[18]), name=chords[20])
gmin_state = yahmm.State(yahmm.DiscreteDistribution(dists[19]), name=chords[21])
gsmin_state = yahmm.State(yahmm.DiscreteDistribution(dists[20]), name=chords[22])
amin_state = yahmm.State(yahmm.DiscreteDistribution(dists[21]), name=chords[23])
asmin_state = yahmm.State(yahmm.DiscreteDistribution(dists[22]), name=chords[24])
bmin_state = yahmm.State(yahmm.DiscreteDistribution(dists[23]), name=chords[25])

caug_state = yahmm.State(yahmm.DiscreteDistribution(dists[24]), name=chords[26])
csaug_state = yahmm.State(yahmm.DiscreteDistribution(dists[25]), name=chords[27])
daug_state = yahmm.State(yahmm.DiscreteDistribution(dists[26]), name=chords[28])
dsaug_state = yahmm.State(yahmm.DiscreteDistribution(dists[27]), name=chords[29])
eaug_state = yahmm.State(yahmm.DiscreteDistribution(dists[28]), name=chords[30])
faug_state = yahmm.State(yahmm.DiscreteDistribution(dists[29]), name=chords[31])
fsaug_state = yahmm.State(yahmm.DiscreteDistribution(dists[30]), name=chords[32])
gaug_state = yahmm.State(yahmm.DiscreteDistribution(dists[31]), name=chords[33])
gsaug_state = yahmm.State(yahmm.DiscreteDistribution(dists[32]), name=chords[34])
aaug_state = yahmm.State(yahmm.DiscreteDistribution(dists[33]), name=chords[35])
asaug_state = yahmm.State(yahmm.DiscreteDistribution(dists[34]), name=chords[36])
baug_state = yahmm.State(yahmm.DiscreteDistribution(dists[35]), name=chords[37])

cdim_state = yahmm.State(yahmm.DiscreteDistribution(dists[36]), name=chords[38])
csdim_state = yahmm.State(yahmm.DiscreteDistribution(dists[37]), name=chords[39])
ddim_state = yahmm.State(yahmm.DiscreteDistribution(dists[38]), name=chords[40])
dsdim_state = yahmm.State(yahmm.DiscreteDistribution(dists[39]), name=chords[41])
edim_state = yahmm.State(yahmm.DiscreteDistribution(dists[40]), name=chords[42])
fdim_state = yahmm.State(yahmm.DiscreteDistribution(dists[41]), name=chords[43])
fsdim_state = yahmm.State(yahmm.DiscreteDistribution(dists[42]), name=chords[44])
gdim_state = yahmm.State(yahmm.DiscreteDistribution(dists[43]), name=chords[45])
gsdim_state = yahmm.State(yahmm.DiscreteDistribution(dists[44]), name=chords[46])
adim_state = yahmm.State(yahmm.DiscreteDistribution(dists[45]), name=chords[47])
asdim_state = yahmm.State(yahmm.DiscreteDistribution(dists[46]), name=chords[48])
bdim_state = yahmm.State(yahmm.DiscreteDistribution(dists[47]), name=chords[49])

states = [c_state, cs_state, d_state, ds_state, e_state, f_state, fs_state, g_state, gs_state, a_state, as_state,
          b_state, cmin_state, csmin_state, dmin_state, dsmin_state, emin_state, fmin_state, fsmin_state, gmin_state,
          gsmin_state, amin_state, asmin_state, bmin_state, caug_state, csaug_state, daug_state, dsaug_state,
          eaug_state, faug_state, fsaug_state, gaug_state, gsaug_state, aaug_state, asaug_state, baug_state, cdim_state,
          csdim_state, ddim_state, dsdim_state, edim_state, fdim_state, fsdim_state, gdim_state, gsdim_state,
          adim_state, asdim_state, bdim_state]

# add state to the model
for state in states:
    model.add_state(state)

# add transitions
for i in range(len(states)):
    model.add_transition(model.start, states[i], transition_matrix[0][i+2])
    model.add_transition(model.end, states[i], transition_matrix[1][i+2])
for i in range(len(chords) - 2):
    for j in range(len(chords) - 2):
        model.add_transition(states[i], states[j], transition_matrix[i+2][j+2])

# bake the model
model.bake( verbose=True )

#write model to stream
file = open('model.txt', 'w')
model.write(file)
file.close()