from binary_search_median import *
import statistics

def test_upper_median():
    assert upper_median_idx([1,2,3,4]) == 2
    assert upper_median_idx([1,2,3]) == 1

def test_lower_median():
    assert lower_median_idx([1,2,3,4]) == 1
    assert lower_median_idx([1,2,3]) == 0
    
def test_minmax_medians_g2():
    test_arrs = [
        [1,2,3,4],
        [5,6,7,8],
        [7,8,9]
    ]
    res = find_minmax_medians(test_arrs)
    low = res[0]
    upp = res[1]

    assert low == (0,1)
    assert upp == (2,1)
    
def test_remove_inclusive_1():
    arrs = [
        [1,2,3],
        [4,5,6]
    ]

    low = (0,1)
    high = (1,1)

    output = remove_els_inclusive(arrs, low, high)
    assert output[0] == [3]
    assert output[1] == [4]

def test_remove_inclusive_2():
    arrs = [
        [1,2,3,4],
        [5,6,7,8]
    ]

    low = (0,1)
    high = (1,2)

    output = remove_els_inclusive(arrs, low, high)
    print(output)
    assert output[0] == [3,4]
    assert output[1] == [5,6]
    
def test_median_search():
    arrs = [
        [1,2,3,4],
        [5,6,7,8]
    ]
    
    big_arr = []
    for arr in arrs:
        big_arr.extend(arr)

    out = median_search(arrs)
    assert out == statistics.median(big_arr)