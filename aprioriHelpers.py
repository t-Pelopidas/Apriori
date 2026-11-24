from operator import index

def create_initial_candidate(dataset_item_labels, dataset_array):
    #C = list[tuple[list[str], int]]
    C = []
    a = dataset_array.shape[0]
    for item in range(len(dataset_item_labels)):
        c = 0
        for t in range(a):
            c += dataset_array[t][item]
        C.append(([dataset_item_labels[item]], int(c)))
    return C

def create_next_candidate(C, k, dataset_item_labels, dataset_array):
    #C = list[tuple[list[str], int]]
    list = []
    C_length = len(C)

    # The distinction is make for k = 1 here so we dont compute the requirement
    # that each combination has to have the first k-1 elements common
    if k == 1:
        for i in range(C_length - 1):
            for j in range(i+1, C_length):
                # This appends both full lists, and not just the names
                list.append(([C[i][0][0], C[j][0][0]], 0))
    else:
        # TODO: replace the for loop with a while, since when and item doesnt find a match in the list, the rest of them arent going to be matches
        for i in range(C_length - 1):
            for j in range(i+1, C_length):
                flag = True
                for t in range(k - 1):
                    if C[i][0][t] != C[j][0][t]:
                        flag = False
                        break
                if flag == True:
                    # append to the list, with the first element of the list in the tuple being the identical items
                    # append to the tuple list the last element of the list we are comparing, since they are the same
                    temp = C[i][0] + [C[j][0][k-1]]
                    list.append((temp, 0))

    populate(list, dataset_item_labels, dataset_array)
    return list

def prune(candidate, min_support):
    c = []
    for i in range(len(candidate)):
        if candidate[i][1] >= min_support:
            c.append((candidate[i][0], candidate[i][1]))
    return c

def get_count(index_list, dataset_array):
    c = 0
    for row in range(dataset_array.shape[0]):
        flag = 1
        for i in index_list:
            flag = flag & int(dataset_array[row][i])
            if flag == 0:
                break
        if flag != 0:
            c += 1
    return c

def populate(C, dataset_item_labels, dataset_array):
    shape = dataset_array.shape
    for i in range(len(C)):
        l = C[i][0]
        index_list = []
        for j in range(len(l)):
            index = dataset_item_labels.index(l[j])
            if index == -1:
                print(f"{l[j]} is not in the dataset. Breaking")
                return -1
            index_list.append(index)
        C[i] = (C[i][0], get_count(index_list, dataset_array))

def calculate_rules(L_k, min_conf):
    rules = []
    for itemset in range(1, len(L_k)):
        pass
    return rules
