import statistics

def lower_median_idx(arr):
    return len(arr)//2 - 1

def upper_median_idx(arr):
    return len(arr)//2

def find_minmax_medians(arrs):
    lowers = []
    uppers = []
    for i,arr in enumerate(arrs):
        m = lower_median_idx(arr)
        n = upper_median_idx(arr)
        lowers.append((arr[m], m, i))
        uppers.append((arr[n], n, i))
        
    lowers.sort()
    uppers.sort(reverse=True)
    low_arr = lowers[0][2]
    low_idx = lowers[0][1]
    upp_arr = uppers[0][2]
    upp_idx = uppers[0][1]
    
    return ((low_arr, low_idx), (upp_arr, upp_idx))
    
def remove_els_inclusive(arrs, low, high):
    # Determine how many elements to remove (we want it the same for both)
    num_els_low = low[1] + 1 # This one is easy
    num_els_high = len(arrs[high[0]]) - high[1]
    
    num_removed = min(num_els_low, num_els_high)
    
    # Do the removal
    del arrs[low[0]][0:num_removed]
    del arrs[high[0]][(len(arrs[high[0]]) - num_removed):]
    return arrs, (low[0], high[0], num_removed)

def remove_els_exclusive(arrs, low, high):
    # Determine how many elements to remove (we want it the same for both)
    num_els_low = low[1] # This one is easy
    num_els_high = len(arrs[high[0]]) - high[1] - 1
    
    num_removed = min(num_els_low, num_els_high)
    
    # Do the removal
    del arrs[low[0]][0:(num_removed-1)]
    del arrs[high[0]][(len(arrs[high[0]]) - num_removed + 1):]
    return arrs, (low[0], high[0], num_removed)

def at_least_three(arrs):
    for arr in arrs:
        if len(arr) < 3:
            return False
    return True

def median_search(arrs):
    lengths = []
    for arr in arrs:
        lengths.append(len(arr))

    while len(arrs) > 2 and all(length > 2 for length in lengths):
        low, high = find_minmax_medians(arrs)
        arrs, (l, h, n) = remove_els_inclusive(arrs, low, high)
        lengths[l] -= n
        lengths[h] -= n

        arrs = [arr for arr in arrs if arr]
        lengths = [length for length in lengths if length > 0]
        
    while at_least_three(arrs):
        low, high = find_minmax_medians(arrs)
        arrs, _ = remove_els_exclusive(arrs, low, high)

    out = []
    for arr in arrs:
        out.extend(arr)
    return statistics.median(out)