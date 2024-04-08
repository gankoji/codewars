from bisect import bisect_left
from bisect import bisect_right

# This is not my solution. The original code came from Fbasham on CodeWars, and 
# they reference the following SO thread for the original description of the algorithm:
# https://stackoverflow.com/questions/6182488/median-of-5-sorted-arrays

def kthOfPiles(givenPiles, k):
    '''
    Perform binary search for kth element in  multiple sorted list

    parameters
    ==========
    givenPiles  a list of (already sorted) lists
    k           the index of the number in the pile we want
    '''
    begins = [0 for _ in givenPiles]
    ends = [len(pile) for pile in givenPiles]
    
    # For each pile
    for pileidx,pivotpile in enumerate(givenPiles):
        
        # Search for the desired value, or until we exhaust this pile
        while begins[pileidx] < ends[pileidx]:
            # Get the midpoint of our current search window
            mid = (begins[pileidx]+ends[pileidx])>>1
            # ... and its value
            midval = pivotpile[mid]
            
            # Then, using binary search (aka bisection)
            # Count up how many elements of each pile are
            smaller_count = 0 # strictly smaller than midval
            smaller_right_count = 0 # less than or equal to midval
            for pile in givenPiles:
                smaller_count += bisect_left(pile,midval) # <
                smaller_right_count += bisect_right(pile,midval) # <=
                
            # If the interval between those two contains k
            if smaller_count <= k and k < smaller_right_count:
                # ... then that's our answer
                return midval
            # Otherwise, we bisect the search window in this pile
            elif smaller_count > k:
                # We've gone too far, cut off the right end
                ends[pileidx] = mid
            else:
                # cut off the left end
                begins[pileidx] = mid+1
            
    return -1

def median_of_arrays(arrs):
    N = sum([len(arr) for arr in arrs])        
    mid_idx = N//2

    midval = kthOfPiles(arrs, mid_idx)
    if N % 2 == 0:
        midval += kthOfPiles(arrs, mid_idx-1)
        midval /= 2

    return midval
