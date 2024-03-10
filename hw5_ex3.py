import timeit
import random

with open('article1.txt', 'r') as file:
    article1_content = file.read()
with open('article2.txt', 'r') as file:
    article2_content = file.read() 

# Функція для обчислення LPS (довжина найбільшого префіксу, що також є суфіксом)
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

# Функція пошуку Кнута-Морріса-Пратта
def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)
    lps = compute_lps(pattern)
    i = j = 0
    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1
        if j == M:
            return i - j
    return -1

# Функція для створення таблиці зсувів для алгоритму Боєра-Мура
def build_shift_table(pattern):
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table

# Функція пошуку Боєра-Мура
def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))
    return -1

# Функція для обчислення поліноміального хешу
def polynomial_hash(s, base=256, modulus=101):
    hash_value = 0
    for char in s:
        hash_value = (hash_value * base + ord(char)) % modulus
    return hash_value

# Функція пошуку Рабіна-Карпа
def rabin_karp_search(main_string, substring):
    base = 256
    modulus = 101
    substring_length = len(substring)
    main_string_length = len(main_string)
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)
    h_multiplier = pow(base, substring_length - 1) % modulus
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i
        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash * base - ord(main_string[i]) * h_multiplier + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus
    return -1



def measure_search_time(func, text, pattern):
    times = timeit.repeat(lambda: func(text, pattern), number=1, repeat=3)
    return min(times)

if __name__ == "__main__":

    existing_substring = "рекомендаційні системи"
    nonexistent_substring = "абабагаламага"

    patterns = [existing_substring, nonexistent_substring]
    functions = [kmp_search, boyer_moore_search, rabin_karp_search]
    articles = [(article1_content, "Стаття 1"), (article2_content, "Стаття 2")]

    print(f"| {'Алгоритм пошуку':<25} | {'Підрядок':<30} | {'Стаття 1 (сек)':<20} | {'Стаття 2 (сек)':<20} |")
    print(f"| {'-'*25} | {'-'*30} | {'-'*20} | {'-'*20} |")

    for pattern in patterns:
        for func in functions:
            times = [measure_search_time(func, article[0], pattern) for article in articles]
            print(f"| {func.__name__:<25} | {pattern:<30} | {times[0]:<20.5f} | {times[1]:<20.5f} |")

