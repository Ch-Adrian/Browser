import numpy as np
import scipy.sparse
import time
import scipy.sparse.linalg
import re

def create_vector(vector_path):
    vec = []
    file = open(vector_path, "r")

    for line in file:
        word, cnt = line.split(" ")
        vec.append((word,int(cnt)))
    file.close()
    
    return vec

def create_model(vector, size):
    model = []
    for i in range(min(size, len(vector))):
        model.append(vector[i])
    return model

def prepare_input(search_input):
    
    model = create_model(create_vector("model_vector.txt"), 200000)

    if len(search_input) < 1:
        return []
    
    search_input = re.findall("[A-Za-z]+[-']?[A-Za-z]+", search_input)
    dict_vec = {}
    dict_model = {}
    
    for i in range(len(model)):
        tmp_word = model[i][0].lower()
        if tmp_word in dict_model:
            tmp = dict_model[tmp_word]
            tmp.append(i)
            dict_model[tmp_word] = tmp
        else:
            dict_model[tmp_word] = [i]
    
    for i in range(len(search_input)):
        if search_input[i] in dict_vec:
            tmp  = dict_vec[search_input[i]]
            dict_vec[search_input[i]] = tmp + 1
        else:
            dict_vec[search_input[i]] = 1
    
    for i in range(len(search_input)):
        search_input[i] = search_input[i].lower()
        if not (search_input[i] in dict_vec):
            dict_vec[search_input[i]] = 1
    
    result_vec = [ 0 for _ in range(200000)]

    for w in dict_model:
        if w in dict_vec:
            for i in range(len(dict_model[w])):
                result_vec[dict_model[w][i]] = 1
    
    r = []
    c = []
    d = []
    for i in range(len(result_vec)):
        if result_vec[i] != 0:
            r.append(i)
            c.append(0)
            d.append(result_vec[i])
    row = np.array(r)
    col = np.array(c)
    data = np.array(d)
    
    return scipy.sparse.csr_matrix((data, (row, col)), shape=(200000,1))

def show_links(result):
    
    file = open("links_final.txt", "r")
    vec = []
    
    for line in file:
        vec.append(line)
    
    links_list = []

    for r in result:
        links_list.append(vec[r[1]][:len(vec[r[1]])-1])
        print(vec[r[1]], end="")
    
    file.close()
    return links_list

def read_sparse(search_input, isIDF=True):
    print("Looking for: ",search_input)
    start = time.time()
    vec = prepare_input(search_input)
    if type(vec) == type([]) and len(vec) == 0:
        return []
    stop = time.time()
    print("Preparation time: ", stop-start)
    
    start = time.time()
    if isIDF == False:
        fileOUT = open("prepared_matrix_with_NORM.txt", "r")
    elif isIDF == True:
        fileOUT = open("prepared_matrix_withNORM_withIDF.txt", "r")

    data = []
    row = []
    col = []

    lin1 = fileOUT.readline()
    for line in fileOUT:
        d,c,r = line.split(" ")
        data.append(float(d))
        col.append(int(c))
        row.append(int(r))
    stop = time.time()
    print("Reading file time: ",stop - start)

    fileOUT.close()

    start = time.time()
    M = scipy.sparse.csr_matrix((data, (row, col)), shape=(200000, 5000))

    result = (vec.transpose()@M).toarray()
    stop = time.time()
    print("Matrix operations time: ", stop-start)

    start = time.time()
    result2 = []
    for i in range(len(result[0])):
        result2.append((result[0][i], i))
    result = sorted(result2, reverse=True)
    stop = time.time()
    print("Sorting time: ", stop - start)
    return show_links(result[:20])

