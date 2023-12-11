import pprint
import random
import numpy
import random

matrix_dimension = pow(5,4)
def define_stochastic_matrix():
    total_tiles = 16.0
    matrix = numpy.full([matrix_dimension,matrix_dimension],0.0)
    #Each element in the matrix will represent the chance of having X number
    #of correct cards selected.
    for i_start in range(0,matrix_dimension):
        start_counts = list(decode(i_start))
        start_tiles = sum(start_counts)
        tiles_left = total_tiles - start_tiles
        for j in range(0,4):
            current_count_in_category = start_counts[j]
            if current_count_in_category < 4:
                prob_of_increasing_count_in_category = (4-current_count_in_category) / tiles_left
                end_counts = [start_counts[0],start_counts[1],start_counts[2],start_counts[3]]
                end_counts[j] += 1
                i_end = encode(end_counts)
                matrix[i_start][i_end] = prob_of_increasing_count_in_category
    return matrix

def define_state_matrix():
    matrix = numpy.full(matrix_dimension,0.0)
    matrix[0] = 1
    return matrix

def find_all_one_aways():
    # This function will find all combinations that contain a 3,
    # i.e. where you are "one away" from having picked all the tiles
    # from a single category, and then will deliver the encoded results.
    results = []
    for i in range(0,matrix_dimension):
        tup = decode(i)
        if tup[0] == 3 or tup[1] == 3 or tup[2] == 3 or tup[3] == 3:
            results.append(i)
    return results

def encode(tuple):
    #This function takes a tuple of length 4 and converts it to
    #an index number for the matrix..
    #Each value in the tuple represents the number of picks that
    #have been made that fall into each category.
    index = 0
    for i in range(0,4):
        index = index + tuple[3-i] * pow(5,i)
    return index

def decode(index):
    #This function takes a matrix index value and converts it to
    #a tuple of length 4.
    #Each value in the tuple represents the number of picks that
    #have been made that fall into each category.
    remainder = index
    results = [0,0,0,0]
    for i in range(0,4):
        results[i]=int(remainder / pow(5,3-i))
        remainder = remainder - results[i] * pow(5,3-i)
    return tuple(results)

# for i1 in range(0,5):
#     for i2 in range(0,5):
#         for i3 in range(0,5):
#             for i4 in range(0,5):
#                 print("(" + str(i1) +", " + str(i2) +", " + str(i3) +", " + str(i4) +") = " + str(encode((i1, i2, i3, i4))) + " = " + str(decode(encode((i1, i2, i3, i4)))))

def markov_chain_method():
    stochastic_matrix = define_stochastic_matrix()
    state_matrix = define_state_matrix()
    for i in range(0,4):
        state_matrix = numpy.matmul(state_matrix,stochastic_matrix)
    one_aways = find_all_one_aways()
    prob_of_one_away = 0;
    for result in range(0,matrix_dimension):
        if result in one_aways:
            prob_of_one_away += state_matrix[result]
    numpy.savetxt('state_matrix.csv',state_matrix,delimiter='\t')
    numpy.savetxt('stochastic_matrix.csv',stochastic_matrix,delimiter='\t')
    print("The probability of getting a 'one away' message when randomly picking 4 tiles is: " + str(prob_of_one_away * 100.0) + "%")

def simulation_method(number_of_trials):
    current_average = 0.0
    i = 0
    for i in range(0,number_of_trials):
        current_trial = do_one_trial()
        current_average = (current_average * i + current_trial) / (i + 1)
    print ("Average from simulation method is " + str(current_average*100) + "%")
    return current_average

def do_one_trial():
    tiles = ['A','A','A','A','B','B','B','B','C','C','C','C','D','D','D','D']
    picks = list(sorted(random.sample(tiles,4)))
    counts = {pick:picks.count(pick) for pick in picks}
    #print("".join(picks))
    one_away = 0
    for category in counts:
        if counts[category] == 3:
            one_away = 1
    return one_away

def go():
    print("We're going to find the probability of getting a ""one away"" message using two different methods.")
    print("First is by using Markov chains to find the exact probability:")
    markov_chain_method()
    print("Now we'll run simulations to confirm that our calculation using Markov chains is accurate:")

    simulation_method(100000000)

go()
