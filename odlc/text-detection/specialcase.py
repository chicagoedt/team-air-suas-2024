'''
    Some special case that help translate the result list generated by easyocr to a more simplified and correct list.

    Basically a rotated P can be read as d or p; a rotated M can be seen as E or W
'''

'''
    Comment: I know it is a messy list BUT I do not know how to come up with an organized way. 

    But I have watched maybe over thousands of images just to come up with this statistics. 

    I hate this job so much. Wish I could have come up with a more organized way but it is hard :(
'''

# helper function for narrowResultList
# Basically if easyOCR returns list [K, K, K, A, K] (meaning K is majority) 
# then we can definitely simplify to list [K]
def majority(letter_list, letter1, letter2, difference):
    if letter_list.count(letter1) > letter_list.count(letter2) + difference:
        return [letter1]
    elif letter_list.count(letter1) + difference < letter_list.count(letter2):
        return [letter2]
    else:
        return [letter1, letter2]

# narrow the list generated by EASYOCR to a more simplified list    
def narrowResultList(result_list):
    letter_list = [i[1] for i in result_list]
    unique_list = list(set(letter_list))

    # INTRO: EASY CASE
    if 'S' in unique_list:
        return ['S']
    if 'B' in unique_list:
        return ['B']
    if 'd' in unique_list or 'p' in unique_list or 'P' in unique_list:
        return ['P']
    if 'E' in unique_list:
        return ['E']
    if 'R' in unique_list:
        return ['R']
    if 'D' in unique_list:
        return ['D']
    if 'J' in unique_list:
        if letter_list.count('J') >= 2:
            return ['J']
    if 'H' in unique_list or 'I' in unique_list:
        if letter_list.count('H') + letter_list.count('I') >= 3:
            return ['H']
    if 'M' in unique_list or 'W' in unique_list:
        if letter_list.count('M') + letter_list.count('W') >= 3:
            return ['M', 'W']

    # BODY: TOUGH CASES
    # case 4, A, V, 1, L, 7
    if '4' in unique_list:
        if 'A' in unique_list:
            return majority(letter_list, '4', 'A', 1)
        elif 'Y' in unique_list:
            return majority(letter_list, 'Y', '4', 1)
        elif 'X' in unique_list:
            return majority(letter_list, '4', 'X', 1)
        elif letter_list.count('4') >= 3:
            return ['4']
        
    if 'A' in unique_list:
        if '4' in unique_list:
            return majority(letter_list, '4', 'A', 1)
        elif 'V' in unique_list:
            return majority(letter_list, 'V', 'A', 1)
        else:
            if 'T' in unique_list:
                return majority(letter_list, 'A', 'T', 0)
            return ['A']
        
    if 'F' in unique_list:
        if 'T' in unique_list:
            return majority(letter_list, 'T', 'F', 1)
        else:
            return ['F']
        
    if 'X' in unique_list:
        if letter_list.count('X') >= 3:
            return ['X']
        elif 'K' in unique_list:
            return majority(letter_list, 'K', 'X', 1)
        elif '4' in unique_list:
            return ['4']
        elif '7' in unique_list or 'V' in unique_list or 'L' in unique_list:
            return ['X']
        
    
    if 'K' in unique_list:
        if letter_list.count('K') >= 2:
            return ['K']
        if 'X' in unique_list:
            return majority(letter_list, 'X', 'K', 1)
        elif 'T' in unique_list:
            return ['T']
    
    if 'T' in unique_list:
        if letter_list.count('T') >= 2:
            return ['T']
    
    if 'Y' in unique_list:
        if '4' in letter_list:
            return majority(letter_list, '4', 'Y', 1)
        else:
            return ['Y']    
    if '1' in unique_list:
        if '7' in unique_list or 'V' in unique_list or 'L' in unique_list:
            return ['1', '7', 'L', 'V']
    
    if letter_list.count('V') >= 3:
        return ['V']
    
    if letter_list.count('L') >= 3:
        return ['L']
    
    if letter_list.count('7') >= 3:
        return ['7']
    
    if ('V' in letter_list and 'L' in letter_list) or ('7' in letter_list and 'L' in letter_list) or ('7' in letter_list and 'V' in letter_list):
        return ['1', 'V', 'L', '7']

    # case special of 0 including Q, C, U, 3
    if 'Q' in unique_list:
        if 'C' in unique_list:
            return majority(letter_list, 'Q', 'C', 0)
        if '8' in unique_list:
            return majority(letter_list, '8', 'Q', 1)
        return ['Q']

    if '8' in unique_list:
        if '3' in unique_list:
            return majority(letter_list, '3', '8', 0)
        return ['8']

    if 'U' in unique_list:
        return ['U']
    
    if '3' in unique_list:
        return ['3']
       
    if 'N' in unique_list or 'Z' in unique_list:
        if 'V' in unique_list:
            return ['V']
        elif '2' in unique_list:
            if letter_list.count('2') > letter_list.count('N') + letter_list.count('Z') + 1:
                return ['2']
            elif letter_list.count('2') + 1 < letter_list.count('N') + letter_list.count('Z'):
                return ['N', 'Z']
            else:
                return ['2', 'N', 'Z']
        elif letter_list.count('N') + letter_list.count('Z') >= 3:
            return ['N', 'Z']
        else:
            return ['N', 'Z']
        
    if '2' in unique_list:
        if letter_list.count('2') <= 1:
            return ['2', 'V']
        else:
            return ['2']
        
    if '5' in unique_list:
        if 'G' in unique_list:
            return majority(letter_list, 'G', '5', 1)
        return ['5']
    
    if 'G' in unique_list:
        return ['G']

    if 'C' in unique_list: # relate to 8, U, C, 
        return ['C']
    
    if '6' in unique_list or '9' in unique_list:
        if letter_list.count('6') + letter_list.count('9') >= 3:
            return ['6', '9']
           
    if '0' in unique_list:
        if letter_list.count('0') >= 6:
            return ['0', 'O']
        else:
            return ['0', 'O', 'Q']
    
    # ENDING: DEALING WITH REDUNDANTS 
    # remove all lowercase results
    for letter in unique_list:
        if letter.isalpha() and letter.islower():
            unique_list.remove(letter)
    
    # deal with couples: 6,9;  M,W;  H,I;  N,Z
    if len(unique_list) == 1:
        if ('6' in unique_list and '9' not in unique_list) or ('6' not in unique_list and '9' in unique_list):
            return ['6', '9']
        elif ('M' in unique_list and 'W' not in unique_list) or ('M' not in unique_list and 'W' in unique_list):
            return ['M', 'W']
        elif ('H' in unique_list and 'I' not in unique_list) or ('H' not in unique_list and 'I' in unique_list):
            return ['H']
        elif ('N' in unique_list and 'Z' not in unique_list) or ('N' not in unique_list and 'Z' in unique_list):
            return ['N', 'Z']
    
    return unique_list
       