import numpy as np
# 1. Create a function that takes dimensions as tuples e.g. (3,3) and a numeric value and returns a Numpy array of the given dimension filled with the given value e.g.: solve((3,3), 5) will return [[5, 5, 5], [5, 5, 5], [5, 5, 5]]

def solve(dimensions, value):
    # Create a Numpy array of the given dimensions filled with the specified value
    array = np.full(dimensions, value)
    return array
print(solve((3,3), 5)) 

# 2. Create a method that takes n Numpy arrays of the same dimensions, sums them and returns the answer
def sum_arrays(*arrays):
    # Check if all arrays have the same shape
    if not all(arr.shape == arrays[0].shape for arr in arrays):
        raise ValueError("All arrays must have the same dimensions.")
    
    # Sum the arrays
    total_sum = np.sum(arrays, axis=0)
    
    return total_sum
print(sum_arrays(np.array([[1, 2], [3, 4]]), np.array([[5, 6], [7, 8]])))  # Should return [[6, 8], [10, 12]]
print(sum_arrays(np.array([[1, 2], [3, 4]]), np.array([[5, 6], [7, 8]]), np.array([[9, 10], [11, 12]])))  # Should return [[15, 18], [21, 24]]
print(sum_arrays(np.array([[1, 2], [3, 4]]), np.array([[5, 6], [7, 8]]), np.array([[9, 10], [11, 12]]), np.array([[13, 14], [15, 16]])))  # Should return [[28, 32], [36, 40]]  

# 3. Given a 2D Array of N X M dimensions, write a function that accepts this array as well as two numbers N and M. The method should return the top-left N X M sub matrix, e.g.: [[1, 2 3], [4, 5, 6], [7, 8, 9]] returns the sum of all the elements in the array

def sum_top_left_submatrix(array, N, M):
    # Check if the provided dimensions are valid
    if N > len(array) or M > len(array[0]):
        raise ValueError("N and M must be within the dimensions of the array.")
    
    # Extract the top-left N x M submatrix
    submatrix = [row[:M] for row in array[:N]]
    
    # Calculate the sum of all elements in the submatrix
    total_sum = sum(sum(row) for row in submatrix)
    
    return total_sum
print(sum_top_left_submatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2, 2))  # Should return 12 (1+2+4+5)    
print(sum_top_left_submatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2, 3))  # Should return 21 (1+2+3+4+5+6)    
print(sum_top_left_submatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 2))  # Should return 27 (1+2+4+5+7+8)    
print(sum_top_left_submatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 3))  # Should return 45 (1+2+3+4+5+6+7+8+9)  
print(sum_top_left_submatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1, 1))  # Should return 1 (1)   
print(sum_top_left_submatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1, 2))  # Should return 3 (1+2) 
print(sum_top_left_submatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2, 1))  # Should return 5 (1+4) 
print(sum_top_left_submatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 1))  # Should return 12 (1+4+7)  
print(sum_top_left_submatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1, 3))  # Should return 6 (1+2+3)   

print(sum_top_left_submatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1:2, 1:3))  # Should return 11 (2+3+5+6)    
print(sum_top_left_submatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2:4, 1:3))  # Should return 29 (5+6+8+9)    
print(sum_top_left_submatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1:3, 1:2))  # Should return 15 (2+5+8)  
print(sum_top_left_submatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2:4, 2:3))  # Should return 15 (6+9)    

# top_left_sub_matrix (matrix, 2, 2) -> should return [[1,2], [4,5]]
def top_left_sub_matrix(array, N, M):
    # Check if the provided dimensions are valid
    if N > len(array) or M > len(array[0]):
        raise ValueError("N and M must be within the dimensions of the array.")
    
    # Extract the top-left N x M submatrix
    submatrix = [row[:M] for row in array[:N]]
    
    return submatrix
print(top_left_sub_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2, 2))  # Should return [[1, 2], [4, 5]]
print(top_left_sub_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2, 3))  # Should return [[1, 2, 3], [4, 5, 6]]
print(top_left_sub_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 2))  # Should return [[1, 2], [4, 5], [7, 8]]
print(top_left_sub_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 3))  # Should return [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(top_left_sub_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1, 1))  # Should return [[1]]  
print(top_left_sub_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1, 2))  # Should return [[1, 2]]   
print(top_left_sub_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2, 1))  # Should return [[1], [4]] 
print(top_left_sub_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 1))  # Should return [[1], [4], [7]]    
print(top_left_sub_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1, 3))  # Should return [[1, 2, 3]]

print(top_left_sub_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1:2, 1:3))  # Should return [[2, 3], [5, 6]]
print(top_left_sub_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2:4, 1:3))  # Should return [[5, 6], [8, 9]]

# 4. Given a 2D Array of N X M dimensions, write a function that accepts this array as well as two numbers N and M. The method should return the bottom-right N X M sub matrix, e.g.: [[1, 2 3], [4, 5, 6], [7, 8, 9]]
def bottom_right_sub_matrix(array, N, M):
    # Check if the provided dimensions are valid
    if N > len(array) or M > len(array[0]):
        raise ValueError("N and M must be within the dimensions of the array.")
    
    # Extract the bottom-right N x M submatrix
    submatrix = [row[-M:] for row in array[-N:]]
    
    return submatrix

# sub_matrix(matrix, 1, 1) -> should return : (Keep in mind these arrays are zero indexed) [[5, 6], [8, 9]]
def sub_matrix(array, N, M):    
    # Check if the provided dimensions are valid
    if N > len(array) or M > len(array[0]):
        raise ValueError("N and M must be within the dimensions of the array.")
    
    # Extract the bottom-right N x M submatrix
    submatrix = [row[-M:] for row in array[-N:]]
    
    return submatrix

print(sub_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1, 1))  # Should return [[9]]
print(sub_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1, 2))  # Should return [[8, 9]]
print(sub_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2, 1))  # Should return [[6], [9]]    
print(sub_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2, 2))  # Should return [[5, 6], [8, 9]]    

# 5. Given a 1D Numpy array. Write a function that accepts this array as parameters. The method should return a dictionary with 'mean' and 'std_dev' as key and array's mean and array's standard deviation as values: [1,1,1]

# solution(arr) - > should return : {'mean': 1.0, 'std_dev': 0.0}
def solution(arr):
    # Calculate mean and standard deviation
    mean_value = arr.mean()
    std_dev_value = arr.std()
    
    # Create a dictionary with the results
    result = {
        'mean': mean_value,
        'std_dev': std_dev_value
    }
    
    return result

print(solution(np.array([1, 1, 1])))  # Should return {'mean': 1.0, 'std_dev': 0.0} 
