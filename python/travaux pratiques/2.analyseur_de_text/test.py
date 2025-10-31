word_list = ['ceci', 'est', 'une', 'phrase', 'ceci', 'est', 'une', 'autre', 'autre', 'ceci', 'est', 'une', 'troisieme', 'phrase']


def calculate_word_occurence(word_list):
    occur_obj = {}
    for word in word_list:
        if(word not in occur_obj):
            occur_obj[word] = 1
        else:
            occur_obj[word] += 1
    return occur_obj

print(calculate_word_occurence(word_list))
