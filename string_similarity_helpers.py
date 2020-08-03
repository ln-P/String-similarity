"""
Set of functions that allow for similar string matching
author:@Wiktor 
"""

import math
import re
import pandas as pd 
from collections import Counter

def jaccard_index(vec1, vec2):
	"""
	Function calculates Jaccard Index between two objects (https://en.wikipedia.org/wiki/Jaccard_index)

    Args:
        vec1 (dict): a dictionary of counted objects, e.g. for string 'economics', vec1 = {'e': 1, 'c': 2, 'o': 2, 'n': 1, 'm': 1, 'i': 1, 's': 1}.
        vec2 (dict): second dictionary of counted objects

    Returns:
        float: Jaccard index.
    """

	vec1_keys = set(vec1.keys())
	vec2_keys = set(vec2.keys())

	intersection = vec1_keys.intersection(vec2_keys)
	numerator = len(intersection) 

	union = vec1_keys.union(vec2_keys)
	denominator = len(union)

	if not denominator:
	    return 0.0
	else:
	    return float(numerator) / float(denominator)

def cosine_similar(vec1, vec2):
    """
    Function calculates Cosine similarity between two objects (https://en.wikipedia.org/wiki/Cosine_similarity)

    Args:
        vec1 (dict): a dictionary of counted objects, e.g. for string 'economics', vec1 = {'e': 1, 'c': 2, 'o': 2, 'n': 1, 'm': 1, 'i': 1, 's': 1}
        vec2 (dict): second dictionary of counted objects

    Returns:
        float: Cosine similarity
    """
    vec1_keys = set(vec1.keys())
    vec2_keys = set(vec2.keys())
    
    intersection = vec1_keys.intersection(vec2_keys)
    numerator = sum([vec1[i] * vec2[i] for i in intersection]) 

    sum1 = sum([vec1[i] ** 2 for i in vec1_keys])
    sum2 = sum([vec2[i] ** 2 for i in vec2_keys])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / float(denominator)

def text_to_ngrams_vector(text, n=2):
    """
    Function creates ngram of an strin and transforms it into count object

    Args:
        text (str): input string that we want to trun into a count vector
        n    (int): number of grams to create

    Returns:
        dict: dictionary of character counts, e.g for string 'economics'; n=2, vec1 = {'ec': 1,'co': 1,'on': 1,'no': 1,'om': 1,'mi': 1,'ic': 1,'cs': 1}
    """
    ngrams = [text[i:i+n] for i in range(len(text)-n+1) if not " " in text[i:i+n]]
    return Counter(ngrams)

def select_best_list(query, choices, score_cutoff = 0.70):
    """
    Function creates list of similar strings based on avaliable choices (inspired by: https://github.com/seatgeek/fuzzywuzzy)

    Args:
        query   (str): input string that we want find matches to 
        choices (list): list of strings (matching candidates)
        score_cutoff (float): cutoff value for matching
    Yields:
        tuple: (<similar_match>, <similarity_score>)
    """
    # Transform query to vector
    query_vec = text_to_ngrams_vector(query)
    
    for choice in choices: 
        # Ignore the same string
        if query == choice:
            continue
        # Calculate similarity between two strings
        choice_vec = text_to_ngrams_vector(choice)
        score = cosine_similar(query_vec, choice_vec)

        if score >= score_cutoff:
            yield (choice, score)

def select_best_one(query, choices, score_cutoff = 0.70):
    """
    Function returns most similar strings based on avaliable choices (inspired by: https://github.com/seatgeek/fuzzywuzzy)

    Args:
        query   (str): input string that we want find matches to 
        choices (list): list of strings (matching candidates)
        score_cutoff (float): cutoff value for matching
    Returns:
        tuple: (<similar_match>, <similarity_score>)

    """
    # Calculate list of the most similar strings
    best_list = select_best_list(query, choices, score_cutoff = score_cutoff)
    
    # Choose most similar string
    try:
        return max(best_list, key=lambda i: i[1])
    except ValueError:
        return ("", 0.0)
