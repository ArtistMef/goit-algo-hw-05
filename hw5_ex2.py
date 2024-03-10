from fractions import Fraction
import random

def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    mid = 0
    iteration = 0
    while low <= high:
        mid = (high + low) // 2
        iteration += 1
        if arr[mid] < x:
            low = mid + 1
        elif arr[mid] > x:
            high = mid - 1
        else:
            return iteration, arr[mid]
    return iteration, arr[high] if high >= x else arr[high + 1]

def random_fractions_generator(n):
    fractions_list = []
    for _ in range(n):
        numerator = random.randint(1, 100)
        denominator = random.randint(1, 100)
        fraction = Fraction(numerator, denominator)
        fractions_list.append(fraction)
    return fractions_list  

def main():
    arr = random_fractions_generator(30)
    arr.sort()
    print(arr)
    x = Fraction(1, 10)
    iterations, upper_bound  = binary_search(arr, x)
    print(f"Iterations = {iterations}, Upper bound: {upper_bound}")
    
if __name__ == "__main__":
    main()