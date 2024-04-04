def sol_username_domain(email):
    ### BEGIN SOLUTION
    ind_at = email.find("@")
    username = email[:ind_at]
    domain = email[ind_at+1:]
    return username, domain

def input_username_domain(num_tests=20):
    from random import choices, choice
    username_options = "abcdefghijklmnop1234567"
    domain_options = ["gmail.com", "outlook.com", "hotmail.com", "yahoo.com"]
    input_values = [[] for i in range(num_tests)]
    args = []
    for i in range(num_tests):
        username = choices(username_options, k=choice([5, 7, 10]))
        username = "".join(username)
        domain = choice(domain_options)
        args.append({"email":username+"@"+domain})
    return input_values, args

def sol_palindrome_checker(word):
    ### BEGIN SOLUTION
    word = word.lower()
    if word == word[::-1]:
        return True
    return False

def input_palindrome_checker(num_tests=20):
    from random import choice, choices
    input_values = [[] for i in range(num_tests)]
    args = []
    options = "abcdefghiABCDEFGHI"
    for i in range(int(num_tests/2)):
        args.append({"word":"".join(choices(options, k=choice([4, 6, 8])))})
    for i in range(num_tests-int(num_tests/2)):
        word = "".join(choices(options, k=choice([3, 5, 7])))
        word = word + word[::-1].lower()
        args.append({"word":word})
    return input_values, args

def sol_complimentary_dna(dna_strand):
    pairs = {"A":"T", "T":"A", "G":"C", "C":"G"}
    ### BEGIN SOLUTION
    compliment = ""
    for letter in dna_strand:
        compliment += pairs[letter]
    return compliment

def input_complimentary_dna(num_tests=30):
    from random import choice, choices
    options = "ATGC"
    input_values = [[] for i in range(num_tests)]
    args = [{"dna_strand":"".join(choices(options, k=choice([6, 10, 14])))} for i in range(num_tests)]
    return input_values, args

def sol_anagram_checker(word1, word2):
    ### BEGIN SOLUTION
    word1 = word1.lower()
    word2 = word2.lower()
    if len(word1) != len(word2):
        return False
    for letter in word1:
        if word1.count(letter) != word2.count(letter):
            return False
    return True

def input_anagram_checker(num_tests=20):
    from random import shuffle, choice, choices
    options = "abcdefghijABCDEFGHIJ"
    input_values = [[] for i in range(num_tests)]
    args = []
    for i in range(int(num_tests/2)):
        word1 = "".join(choices(options, k=choice([4, 6, 8])))
        word2 = "".join(choices(options, k=choice([4, 6, 8])))
        args.append({"word1":word1, "word2":word2})
    for i in range(num_tests - int(num_tests/2)):
        word1 = "".join(choices(options, k=choice([4, 6, 8])))
        anagram = list(word1)
        shuffle(anagram)
        anagram = "".join(anagram)
        args.append({"word1":word1, "word2":anagram.lower()})
    return input_values, args
