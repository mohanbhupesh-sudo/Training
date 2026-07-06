# Create a list containing squares of numbers from 1 to 10 (HINT: use list comprehension)
squares = [x**2 for x in range(1, 11)]
print("Squares of numbers from 1 to 10:", squares)

# Write a function to check if the year number is a leap year or not. A leap year is divisible by 4, but not divisible by 100, unless it is also divisible by 400.
def is_leap_year(year):
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        return True
    else:
        return False

print(is_leap_year(2020))  # True
print(is_leap_year(1900))  # False
print(is_leap_year(1947))  # False

# Write a function to take an array and return another array that contains the members of the first array that are even
def get_even_numbers(arr):
    return [x for x in arr if x % 2 == 0]

print(get_even_numbers([1, 2, 3, 4, 5, 6]))  # [2, 4, 6]
print(get_even_numbers([7, 8, 9, 10]))  # [8, 10]
print(get_even_numbers([11, 12, 13, 14, 15]))  # [12, 14]

# Write a function that takes 2 arrays and prints the members of the first array that are present in the second array. (HINT: use membership comprehension)
def print_common_elements(arr1, arr2):
    common_elements = [x for x in arr1 if x in arr2]
    print("Common elements:", common_elements)

print_common_elements([1, 2, 3, 4], [3, 4, 5, 6])  # Common elements: [3, 4]
print_common_elements(['a', 'b', 'c'], ['b', 'c', 'd'])  # Common elements: ['b', 'c']
print_common_elements([10, 20, 30], [15, 25, 30])  # Common elements: [30]
print_common_elements([1, 2, 3], [4, 5, 6])  # Common elements: []


