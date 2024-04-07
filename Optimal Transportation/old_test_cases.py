cases = []
suppliers = [1,2]
consumers = [2,1]
costs = [
    [3,4],
    [1,2]
]
expected = 6
cases.append([suppliers, consumers, costs, expected])

suppliers = [10, 7, 13]
consumers = [6, 20, 4]
costs = [
    [4, 12, 3],
    [20, 1, 6],
    [7, 0, 5]
]
expected = 43
cases.append([suppliers, consumers, costs, expected])

suppliers = [8, 15, 21]
consumers = [8, 36]
costs = [
    [9, 16],
    [7, 13],
    [25, 1]
]
expected = 288
cases.append([suppliers, consumers, costs, expected])

suppliers = [31, 16]
consumers = [14, 17, 16]
costs = [
    [41, 18, 0],
    [4, 16, 37]
]
expected = 358
cases.append([suppliers, consumers, costs, expected])

suppliers = [10, 20, 20]
consumers = [5, 25, 10, 10]
costs = [
    [2, 5, 3, 0],
    [3, 4, 1, 4],
    [2, 6, 5, 2]
]
expected = 150
cases.append([suppliers, consumers, costs, expected])

suppliers = [13, 44, 27, 39, 17]
consumers = [28, 12, 30, 17, 19, 34]
costs = [
    [6, 6, 12, 8, 13, 13],
    [7, 20, 5, 16, 11, 16],
    [4, 6, 19, 0, 2, 18],
    [1, 16, 6, 11, 8, 11],
    [5, 6, 11, 1, 6, 14]
]
expected = 759
cases.append([suppliers, consumers, costs, expected])

suppliers = [241, 13]
consumers = [104, 29, 23, 5, 2, 4, 3, 39, 45]
costs = [
    [9, 88, 1, 68, 1, 48, 70, 85, 61],
    [23, 73, 44, 59, 81, 23, 2, 9, 41]
]
expected = 9327
cases.append([suppliers, consumers, costs, expected])

suppliers = [11, 20, 28, 117]
consumers = [26, 73, 77]
costs = [
    [67, 31, 18],
    [12, 15, 31],
    [37, 21, 70],
    [36, 96, 26]
]
expected = 5511
cases.append([suppliers, consumers, costs, expected])