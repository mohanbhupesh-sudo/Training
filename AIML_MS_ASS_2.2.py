# Q1. Mathematical Operators   
# Note: Rectangle: Area = l × w, Perimeter = 2(l + w) (where l is length, w is width))
print('Mathematical Operators')
def q1_area_perimeter(length, width):
    varea = length * width
    vperimeter = 2 * (length + width)
    output = (f'Area: {varea}, Perimeter: {vperimeter}')
    return output
vlength = int(input('Enter Length : '))
vwidth = int(input('Enter Width : '))
print(q1_area_perimeter(vlength, vwidth))

# Q2. Arithmetic Operations
print('Arithmetic Operations ')
def q2_arithmetic(a, b):
    return {
        'addition': a + b,
        'subtraction': a - b,
        'multiplication': a * b,
        'division_float': a / b if b != 0 else None,
        'division_int': a // b if b != 0 else None,
        'modulus': a % b if b != 0 else None,
        'exponent': a ** b,
    }
a = int(input('Enter First Number: '))
b = int(input('Enter Second Number: '))
print(q2_arithmetic(a, b))

# Q3. Operator Precedence
print('Operator Precedence')
def q3_operator_precedence():
    result = 10 + 3 * 2 ** 2
    explanation = 'Exponent > Multiplication > Addition'
    return result, explanation
print(q3_operator_precedence())

# Q4. Even or Odd
print('Even or Odd ')
def q4_even_odd(n):
    return 'Even' if n % 2 == 0 else 'Odd'

n = int(input('Enter Numeric value: '))
print( q4_even_odd(n))

# Q5. Maximum of Three Numbers
print('Maximum of Three Numbers ')
def q5_max_of_three(a, b, c):
    return max(a, b, c)
a = int(input('Enter First Number: '))
b = int(input('Enter Second Number: '))
c = int(input('Enter Third Number: '))
print(q5_max_of_three(a, b, c))

# Q6. Grading System
print('Grading System ')
def q6_grade(marks):
    if marks >= 90:
        return 'Grade A'
    if marks >= 75:
        return 'Grade B'
    if marks >= 50:
        return 'Grade C'
    return 'Grade F'
marks = int(input('Enter student marks: '))
print(q6_grade(marks))

# Q7. Leap Year Checker
print('Leap Year Checker')
def q7_leap_year(year):
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return 'Leap Year'
    return 'Not Leap Year'
year= int(input('Enter the Year for Leap Year Validation: '))
print(q7_leap_year(year))

# Q8. Simple Calculator:
print('Simple Calculator')
def q8_calculator(a, b, op):
    if op == '+':
        return a + b
    if op == '-':
        return a - b
    if op == '*':
        return a * b
    if op == '/':
        return a / b if b != 0 else None
    return None
a = int(input('Enter first value: '))
b = int(input('Enter Second Value: '))
op = input('Enter operator: ')
print(q8_calculator(a, b, op))