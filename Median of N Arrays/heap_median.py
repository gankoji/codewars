import heapq

def heap_median(arrs):
    els = []
    n = sum([len(arr) for arr in arrs]) 

    for i, arr in enumerate(arrs):
        el = arr.pop(0)
        els.append((el,i))
        
    k = n//2
    odd = (n%2 != 0)
    # print(f'N for heaps: {n}, k: {k}, odd: {odd}')

    heapq.heapify(els)

    i = 0
    el = new_el = 0

    while i < k:
        el,j = heapq.heappop(els)
        if arrs[j]:
            new_el = arrs[j].pop(0)
        else:
            del arrs[j]
            new_el, j = heapq.heappop(els)
        heapq.heappush(els, (new_el, j))
        i += 1

    if odd:
        return el
    else:
        return (el+new_el)/2.
