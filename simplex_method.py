simplex_table = [[0.9, 1.1, 0.7, 1.3, 70],
                 [1.2, 1.5, 0.9, 1.1, 55],
                 [1.3, 1.5, 0.9, 1.2, 35],
                 [1, 0, 0, 0, 87],
                 [0, 1, 0, 0, 67],
                 [0, 0, 1, 0, 110],
                 [0, 0, 0, 1, 45],
                 [-33, -39, -36, -43, 0]
                 ]

coefficients_of_objective_function_basic = [33, 39, 36, 43]
coefficients_of_objective_function_non_basic = [0, 0, 0, 0, 0, 0, 0]


# Function to find the column for the entering variable (minimum in the last row)
def find_variable_to_include_in_basis():
    index = -1
    num_of_rows = len(simplex_table)
    min_value = 0  # We're looking for negative values in the objective function row

    for i in range(len(simplex_table[0]) - 1):  # Skip the last column (free term)
        if simplex_table[num_of_rows - 1][i] < min_value:  # Find minimum negative value
            min_value = simplex_table[num_of_rows - 1][i]
            index = i

    return index


# Function to find the row for the exiting variable (minimum positive ratio)
def find_variable_to_exclude_from_basis(index_of_corresponding_col):
    index = -1
    index_of_last_col = len(simplex_table[0]) - 1
    ratio_free_terms_to_corresponding_positive_elements = []

    for row in simplex_table[:-1]:  # Exclude the last row (objective function)
        if row[index_of_corresponding_col] > 0:  # Only consider positive elements in the column
            ratio = row[index_of_last_col] / row[index_of_corresponding_col]
            ratio_free_terms_to_corresponding_positive_elements.append(ratio)
        else:
            ratio_free_terms_to_corresponding_positive_elements.append(float('inf'))  # Impossible ratio

    min_value = float('inf')
    for i in range(len(ratio_free_terms_to_corresponding_positive_elements)):
        if ratio_free_terms_to_corresponding_positive_elements[i] < min_value:
            min_value = ratio_free_terms_to_corresponding_positive_elements[i]
            index = i

    return index


# Rectangular Rule to update the simplex table based on pivot
def rectangular_rule(r, n):
    pivot_element = simplex_table[r][n]
    new_table = [row[:] for row in simplex_table]  # Copy table to avoid in-place modification issues

    # Normalize the pivot row
    for j in range(len(simplex_table[0])):
        new_table[r][j] /= pivot_element

    # Update all other rows based on the normalized pivot row
    for i in range(len(simplex_table)):
        if i != r:
            row_factor = simplex_table[i][n]
            for j in range(len(simplex_table[0])):
                new_table[i][j] -= row_factor * new_table[r][j]

    return new_table


# Swap the basic and non-basic variables
def swap_variables(row, col):
    tmp = coefficients_of_objective_function_basic[col]
    coefficients_of_objective_function_basic[col] = coefficients_of_objective_function_non_basic[row]
    coefficients_of_objective_function_non_basic[row] = tmp


# Main Simplex method
def simplex_method():
    iter = 0
    while True:
        variable_to_include_in_basis = find_variable_to_include_in_basis()
        if variable_to_include_in_basis == -1:  # No negative values, optimal solution found
            print("Optimal solution found.")
            break

        print('Iteration:', iter)
        iter += 1

        variable_to_exclude_from_basis = find_variable_to_exclude_from_basis(variable_to_include_in_basis)
        if variable_to_exclude_from_basis == -1:  # No valid pivot found, problem is unbounded
            print("The solution is unbounded.")
            break

        # Perform rectangle rule updates
        global simplex_table
        simplex_table = rectangular_rule(variable_to_exclude_from_basis, variable_to_include_in_basis)

        swap_variables(variable_to_exclude_from_basis, variable_to_include_in_basis)

        for row in simplex_table:
            print(row)
        print()


# Run the Simplex method
simplex_method()
