import numpy

# Load the probability matrix.
transition_matrix = numpy.loadtxt(open("data/matrix.csv", "rb"), delimiter=",")

# How many matrices to make.
create_to = 50

for r in range(1, create_to + 1):
    matrix = numpy.zeros((41, 41))

    for roll in range(1, r + 1):
        new_matrix = numpy.linalg.matrix_power(transition_matrix, roll)  # Raise the matrix to the roll power.
        matrix = numpy.add(matrix, new_matrix)

    numpy.savetxt("data/t" + str(r) + ".csv", matrix, delimiter=",")