#!/usr/bin/env python
# coding: utf-8

# In[1]:


#
# 6G7Z1003 portfolio assignment
# python implementation of ACO tour construction using I-Roulette 
#
import numpy as np
import random
import time
import multiprocessing as mp

def check_tour( tour, n ):
    # sanity check a tour to make sure it has each city represented once
    m = len(tour)
    if m != n:
        return False
    counts = [0 for i in range(n)]
    for city in tour:
        if city < 0 or city > n-1 or counts[city] != 0:
            return False
        counts[city] += 1
    return True

def check_tours( tours, n ):
    # check all tours in a list
    all_valid = True
    for t in tours:
        if not check_tour(t, n):
            all_valid = False
            break
    return all_valid

#------------------------------------
# Serial version.

def iroulette( weights ): # This function requires the 1d array of weights that has been constructed in the for loop 
                          # within the contruct_tour function right below. 
    # Independent roulette - multiply weights by random numbers and return index of highest product
    num_weights = len(weights) # num_weights is the size of the 1d array weights. 
    imax = -1; # imax is initialised to -1. It is intended to keep the index of the weights' element 
               # that yielded max. product.
    vmax = 0 #vmax is initialised to 0. It is intended to keep the maximum product. 
    for i in range(num_weights): #for loop to iterate over the elements of weights.  
        val = weights[i]* random.random() # val is assigned the calculation of the product: weights' elements 
                                          # to a uniformly distributed random number.  
        if val > vmax:   # evaluates True if the new calculated product (val) is strictly bigger than vmax.
            vmax = val # in case val>vmax, vmax will be updated by the new product.
            imax = i #imax is updated by assigning the index of the corresponding highest product. 
    return imax # This function outputs the index of the highest product. 
    
def construct_tour( weights ): # The construct_tour's input is the weights matrix defined in the main() function. 
    # plain python version - construct a tour using the iroulette function
    n = weights[0].size     # n represents the number of cities in the TSP problem. It is deduced here from 
                            # the input variable weights (equals to the number of elements of the first row 
                            # of the weights matrix).  
    # random start city
    cur_city = random.randrange(0,n)   # The start city will be chosen randomly within the range of all cities 
                                       # by using the randrange method of the library random.
    tour = [cur_city]   # The tour list is initialised with the start city, and will be appended, 
                        # within the while loop below, with the next city for visit in each iteration. 
    # free[i] is true if city i has not been visited 
    free = np.zeros(n) == 0.0   # The free structure is a list of booleans which is created by using the condition 
                                # on equality of a predefined array of zeros of size n to the float 0.0 
                                # and that produces a list of booleans with the value "True". 
    free[cur_city] = False       # Set the element corresponding to the index "cur_city" in the free array to "False" 
                                 # as this is the start city (i.e., visisted city). 
        
    while len(tour) < n:
        w = []           # w represents a list of weights assigned to the edges connecting the current city 
                         # (current position of the ant) and the remaining cities that have been visited yet. 
                         # It is initialised to an empty list, here, for each iteration within the while loop.
        indices = []     # indices is a list that keeps track of the cities' indices and follows 
                         # the weights list w for appending within the for loop below. It is initialised 
                         # to an empty list, here, for each iteration within the while loop.
        for i in range(n): # for loop to iterate over the sequence of n cities.
            if free[i]: # Evaluates True if the city i has not been visited yet by the ant.
                w.append( weights[cur_city][i] ) # w is appended with the weight connecting the current city to the city i 
                                                 # by indexing the weights matrix.  
                indices.append(i)                # indices is appended with the index of the city i. 
        sel = iroulette(w)   # sel represents the position corresponding to the maximum product "weight*random" which is
                             # evaluated by calling the function "iroulette". 
        cur_city = indices[sel] # the variable "cur_city" is updated by the next city to be visited 
                                # which is selected by indexing the indices list using the sel variable. 
        tour.append(cur_city)   # tour is appended by the variable cur_city (i.e. next city for visit). 
        free[cur_city] = False  # The free array is updated by assigning the value False to the index 
                                # corresponding to the cur_city.
    return tour # The output of this construct_tour function is the tour list. 

def construct_tours( weights, num_ants ): #This function requires the 2d array "weight" and the number of ants as inputs. 
    # construct num_ants tours, and return in a list
    tours = [] # The tours variable is initialised with an empty list, and will be appended, within the for loop below
               # with the next tour constructed in each iteration.
    for i in range(num_ants): # for loop to iterate over the number of ants. 
        tours.append( construct_tour(weights)) #tours is appended with the next tour by calling the function "construct_tour".
    return tours # The output is a list of tours. 

# --------------------------------------------------------
# Vectorised version of the given problem using Numpy.

def np_construct_tour( weights ):
# todo: make this construct a tour from the weights, using a vectorized version of I-Roulette
    n = weights[0].size     # n represents the number of cities in the TSP problem. It is deduced here from 
                            # the input variable weights (equals to the number of elements of the first row 
                            # of the weights matrix).  
    # random start city
    cur_city = random.randrange(0,n)   # The start city will be chosen randomly within the range of all cities 
                                       # by using the randrange method of the library random.
    tour = np.full(n,0)    # tour is initialised by constructing a numpy array of size n (i.e., number of cities) 
                           # that is populated by the integer 0 using the numpy method full.
    tour[0]=cur_city    # The cur_city is assigned to the first element of the array tour. 
    # free[i] is true if city i has not been visited 
    free= np.zeros(n) == 0.0  # The free structure is a list of booleans which is created 
                              # by using the condition on equality of a predefined array of zeros of size n 
                              # to the float 0.0 and that produces a list of booleans with the value "True".
    free[cur_city] = False   # Set the element corresponding to the index "cur_city" in the free array to "False" 
                             # as this is the start city (i.e., visisted city). 

    i=1  # i is a counter that will help to assign cities to the tour array.  
    while i < n: # Evaluates true if there are still cities that have not been visited. 
        w = weights[cur_city][free] # w is obtained by boolean indexing the list "weights[cur_city]" using the list "free". 
        indices = np.arange(n)[free] # indices is obtained by boolean indexing, using the list "free", the list of integers 
                                     # (0 to n-1) generated by the numpy built-in "np.arange".
        sel = np.argmax(w*random.random()) # The variable sel is vectorised by using the numpy built-in "np.argmax" 
                                           # to return the position that corresponds to the maximum value 
                                           # within the output of the product "w*random.random()".
        cur_city = indices[sel] # the variable "cur_city" is updated by the next city to be visited 
                                # which is selected by indexing the indices list using the "sel" variable.
        tour[i]=cur_city # the new "cur_city" is assigned to the next element (element i) of the tour array. 
        i+=1 # The counter i is incremented by 1.
        free[cur_city] = False  # The free array is updated by assigning the value False to the index 
                                # corresponding to the cur_city.
    return tour.tolist() # The data structure of the output "tour" (numpy array) is converted to a list to show similarity 
                         # with the output of the serial code. 
    
def construct_tours_np( weights, num_ants ):
    # construct num_ants tours using the numpy vesion of the tour construction function, and return in a list
    tours = []
    for i in range(num_ants):
        tours.append( np_construct_tour(weights) )
    return tours

# --------------------------------
# Parallel version of the given problem using multiprocessing.
# todo: use multiprocessing to construct tours in parallel (using np_construct_tour) 

def my_func(weights,q): # This is just a small function that allows the "np_construct_tour" function to use the put method.
                        # In addition to the argument "weights", "q" is needed for the put method.
    q.put(np_construct_tour(weights)) # The put method is used to insert the output of the evaluation of the function
                                      # "np_construct_tour" to the Queue object. 

def construct_tours_mp( weights, num_ants ):
    num_procs = num_ants # The number of ants is assigned to the number of processes that run in parallel.
    out_queue = mp.Queue() # The object QUEUE of the module multiprocessing is assigned the variable "out_queue".
    
    procs = [mp.Process(target=my_func,args=(weights,out_queue)) for p in range(num_procs)] # processes are spawned 
        # using the method "Process" of the multiprocessing library with the target function "my_func"
        # and the arguments "weights" and "out_queue". Those processes are created in a comprehension list     
        # which is assigned to the variable "procs". 
                                        
    for p in procs:  # "for loop" to iterate over the processes.
        p.start()    # "start" method allows to start the processes.
    
    tours=[out_queue.get() for p in procs] # printing elements of the object "Queue" for all the processes using get method
                                           # in a comprehension list which is assigned to the variable "tours".
    return tours  # printing the variable "tours".

#---------------------------------
def main():
    n = 1000 # number of cities in the problem
    weights = np.random.random((n,n)) # square matrix of random weights for edges
    num_ants = 8

      # run the plain python version
    t = time.perf_counter()
    tours = construct_tours( weights, num_ants)
    t = time.perf_counter() - t
    print("constructed",len(tours),"tours")
    print("valid tours:",check_tours(tours, n))
    print("Serial: time for",num_ants,"ants is",t)
    print()
    
       # run the numpy version - you need to implement this
    t = time.perf_counter()
    tours = construct_tours_np( weights, num_ants )
    t = time.perf_counter() - t
    print("constructed",len(tours),"tours")
    print("valid tours:",check_tours(tours, n))
    print("Numpy: time for",num_ants,"ants is",t)
    print()
    
      # run the multiprocessing version - you need to implement this
    t = time.perf_counter()
    tours = construct_tours_mp( weights, num_ants )
    t = time.perf_counter() - t
    print("constructed",len(tours),"tours")
    print("valid tours:",check_tours(tours, n))
    print("Multiprocessing: time for",num_ants,"ants is",t)   

if __name__ == '__main__':
    main()

