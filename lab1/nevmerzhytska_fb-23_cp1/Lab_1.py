import math
from collections import Counter
import re

russian_alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

def calculate_entropy(probabilities):
    return -sum(p * math.log2(p) for p in probabilities if p > 0)

def calculate_redundancy(H, N):
    return 1 - (H / math.log2(N))

def preprocess_text(text):
    cleaned = ''.join([ch.lower() for ch in text if ch in russian_alphabet + ' '])
    while '  ' in cleaned:
        cleaned = cleaned.replace('  ', ' ')
    return cleaned

def count_bigram_frequencies(text, step=1):
    string = ''.join(text)
    bigram_frequencies = {}
    for i in range(0, len(string) - 1, step):
        bigram = string[i:i + 2]
        if bigram in bigram_frequencies:
            bigram_frequencies[bigram] += 1
        else:
            bigram_frequencies[bigram] = 1
    return bigram_frequencies

def calculate_H(bigram_frequencies):
    total_bigrams = sum(bigram_frequencies.values())
    probabilities = [freq / total_bigrams for freq in bigram_frequencies.values()]
    return calculate_entropy(probabilities)

def analyze_text(text):
    text = preprocess_text(text)

    letter_count = Counter(text)
    total_letters = sum(letter_count.values())
    letter_probabilities = [count / total_letters for count in letter_count.values()]

    H1 = calculate_entropy(letter_probabilities)
    N_letters = len(letter_count)
    redundancy_letters = calculate_redundancy(H1, N_letters)

    bigram_frequencies = count_bigram_frequencies(text)
    bigram_frequencies_no_overlap = count_bigram_frequencies(text, step=2)

    H2 = 0.5 * calculate_H(bigram_frequencies)
    H2_no_overlap = 0.5 * calculate_H(bigram_frequencies_no_overlap)

    N_bigrams = len(letter_count) ** 2
    redundancy_bigrams = calculate_redundancy(H2, N_bigrams)
    redundancy_bigrams_no_overlap = calculate_redundancy(H2_no_overlap, N_bigrams)

    return (letter_count, bigram_frequencies, bigram_frequencies_no_overlap, H1, H2, H2_no_overlap, 
            redundancy_letters, redundancy_bigrams, redundancy_bigrams_no_overlap)


def analyze_text_without_spaces(text):
    text_without_spaces = preprocess_text(text).replace(' ', '')
    return analyze_text(text_without_spaces)


def read_text_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()


def write_cleaned_text_to_file(input_filename, output_filename):
    text = read_text_from_file(input_filename)
    cleaned_text = preprocess_text(text)
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)


def count_character_frequencies(lst):
    char_freq = {}
    for char in lst:
        if char in char_freq:
            char_freq[char] += 1
        else:
            char_freq[char] = 1
    return char_freq

def count_bigram_frequencies_step(lst, step=1):
    string = ''.join(lst)
    bigr_freq = {}
    for i in range(0, len(lst)-1, step):
        bigr = string[i:i+2]
        if bigr in bigr_freq:
            bigr_freq[bigr] += 1
        else:
            bigr_freq[bigr] = 1
    return bigr_freq

def calculate_R(entr, length=34):
    R = 1 - (entr / math.log2(length))
    return R

input_file = 'text1.txt'
cleaned_file = 'cleaned_text1.txt'
write_cleaned_text_to_file(input_file, cleaned_file)

text = read_text_from_file(cleaned_file)

letter_count, bigram_frequencies, bigram_frequencies_no_overlap, H1, H2, H2_no_overlap, redundancy_letters, redundancy_bigrams, redundancy_bigrams_no_overlap = analyze_text(text)

print("\nЧастота букв у тексті:")
letter_table = [(letter, count, count / sum(letter_count.values())) for letter, count in letter_count.items()]
letter_table.sort(key=lambda x: x[1], reverse=True)
for letter, count, frequency in letter_table:
    print("{:<10} {:<10} {:<10.5f}".format(letter, count, frequency))

print("\nЧастота біграм в тексті з перетинами:")
bigram_table = [(bigram, count, count / sum(bigram_frequencies.values())) for bigram, count in bigram_frequencies.items()]
bigram_table.sort(key=lambda x: x[1], reverse=True)
for bigram, count, frequency in bigram_table:
    print("{:<10} {:<10} {:<10.5f}".format(bigram, count, frequency))

print("\nЧастота біграм в тексті без перетинів:")
bigram_no_overlap_table = [(bigram, count, count / sum(bigram_frequencies_no_overlap.values())) for bigram, count in bigram_frequencies_no_overlap.items()]
bigram_no_overlap_table.sort(key=lambda x: x[1], reverse=True)
for bigram, count, frequency in bigram_no_overlap_table:
    print("{:<10} {:<10} {:<10.5f}".format(bigram, count, frequency))

print("\nЕнтропія для символів з пробілами:", H1)
print("Ентропія для символів без пробілів:", analyze_text_without_spaces(text)[3])
print("Ентропія для біграм з пробілами і перетинами:", H2)
print("Ентропія для біграм з пробілами без перетинів:", H2_no_overlap)
print("Ентропія для біграм без пробілів з перетинами:", analyze_text_without_spaces(text)[4])
print("Ентропія для біграм без пробілів без перетинів:", analyze_text_without_spaces(text)[5], "\n")


finish, finish_with = list(preprocess_text(text).replace(' ', '')), list(preprocess_text(text))
print("Надлишковість для символів  з пробілами: ", calculate_R(calculate_H(count_character_frequencies(finish_with))))
print("Надлишковість для символів  без пробілів: ", calculate_R(calculate_H(count_character_frequencies(finish)), 33))
print("Надлишковість для біграм з пробілами і перетинами: ", calculate_R(0.5 * calculate_H(count_bigram_frequencies_step(finish_with))))
print("Надлишковість для біграм з пробілами без перетинів: ", calculate_R(0.5 * calculate_H(count_bigram_frequencies_step(finish_with, 2))))
print("Надлишковість для біграм без пробілів з перетинами: ", calculate_R(0.5 * calculate_H(count_bigram_frequencies_step(finish)), 33))
print("Надлишковість для біграм без пробілів без перетинів: ", calculate_R(0.5 * calculate_H(count_bigram_frequencies_step(finish, 2)), 33))
