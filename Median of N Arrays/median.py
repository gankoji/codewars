import statistics
import copy
import random
import time
import numpy as np

from binary_search_median import median_search

def median_from_n_arrays(arrays):
    big_arr = []
    for arr in arrays:
        big_arr.extend(arr)
    
    return statistics.median(big_arr)

def median_from_n_arrays_search(arrays):
    return median_search(arrays)

import codewars_test as test

@test.describe("Basic Tests")
def test_group():
    @test.it("2 Arrays")
    def test_case():
        test.assert_equals(median_from_n_arrays([[5,7,9],[7,10,11,13]]), 9)
        test.assert_equals(median_from_n_arrays([[10,11,12],[14,20,40]]), 13)
    @test.it("3 Arrays")
    def test_case():
        test.assert_equals(median_from_n_arrays([[20,30,40,50,60],[70,80],[90,100]]), 60)
        test.assert_equals(median_from_n_arrays([[1,8,10],[2,3,4],[12,20]]), 6)
    @test.it("Edge Cases")
    def test_case():
        test.assert_equals(median_from_n_arrays([[],[2,3,4]]), 3)
        test.assert_equals(median_from_n_arrays([[10,15,20],[22,26,30]]), 21)
        
    @test.it("Speed Test Cases")
    def test_case():
        test_arrays_1 = [sorted([random.randrange(1,1000) for _ in range(20)]) for _ in range(5)] 
        test_arrays_2 = [sorted([random.randrange(1,1000) for _ in range(1000)]) for _ in range(10)] 
        test_arrays_3 = [sorted([random.randrange(1,1000) for _ in range(2000000)]) for _ in range(15)] 
        test_arrays_4 = copy.deepcopy(test_arrays_3)
        
        print('Finshed generating data, beginning test.')
        start = time.time()
        median_from_n_arrays(test_arrays_1)
        print(f'5x20 arrays took {time.time() - start} seconds.')
        start = time.time()
        median_from_n_arrays(test_arrays_2)
        print(f'10x1000 arrays took {time.time() - start} seconds.')
        start = time.time()
        res = median_from_n_arrays(test_arrays_3)
        print(f'15x2000000 arrays took {time.time() - start} seconds with the basic alg.')
        start = time.time()
        res2 = median_search(test_arrays_4)
        print(f'15x2000000 arrays took {time.time() - start} seconds with the search alg.')
        print(f'Different alg results: {res} vs {res2}')