import numpy

# Load the probability matrix.
transition_matrix = numpy.loadtxt(open("data/matrix.csv", "rb"), delimiter=",")


def add_matrices():
    # How many matrices to make.
    create_to = 100

    for r in range(1, create_to + 1):
        matrix = numpy.zeros((41, 41))

        for roll in range(1, r + 1):
            new_matrix = numpy.linalg.matrix_power(transition_matrix, roll)  # Raise the matrix to the roll power.
            matrix = numpy.add(matrix, new_matrix)

        numpy.savetxt("data/t" + str(r) + ".csv", matrix, delimiter=",")


def long_time():
    new_matrix = numpy.linalg.matrix_power(transition_matrix, 1000)
    numpy.savetxt("data/longtime.csv", new_matrix, delimiter=",")
    for i in new_matrix[0]:
        print(i)

def create_powers():
    for power in range(100):
        new_matrix = numpy.linalg.matrix_power(transition_matrix, power)
        numpy.savetxt("data/p" + str(power) + ".csv", new_matrix, delimiter=",")


long_time()
add_matrices()
create_powers()