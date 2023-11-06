# (a)
def p(n: str) -> str:
    return f"a_{{{n}}} < 1"

base = "a_{0} = 1/5 < 1."

def step(n: str, pn_name: str) -> str:
    return f"a_{{{n} + 1}} = (1 + a_{{{n}}}) / 2 < (1 + 1) / 2 (from {pn_name}) = 1."

# (b)
def SI(p_function, base_string, step_function):
    proof = "Base Case: " + base_string + "\n"
    proof += "Inductive Step: Let n ∈ N. Assume (IH) " + p_function('n') + ".\n"
    proof += step_function('n', "(IH)") + "\n"
    return proof

def WOP(p_function, base_string, step_function):
    proof = "Assume, for contradiction, there is an n ∈ N where " + p_function('n') + " is false.\n"
    proof += "Let C = { n ∈ N : " + p_function('n') + " is false }.\n"
    proof += "Then C ⊆ N and by the assumption is non−empty.\n"
    proof += "So C has a minimum element m.\n"
    proof += "Then " + p_function('m') + " is false but " + p_function('n') + " is true for each natural n < m.\n"
    proof += "Case m = 0: But " + base_string + " contradicting that " + p_function('m') + " is false.\n"
    proof += "Case m > 0: Then m − 1 < m, and m − 1 ∈ N since m > 0, so " + p_function('m - 1') + ".\n"
    proof += step_function('m - 1', p_function('m - 1')) + "\n"
    proof += "But m = m − 1 + 1, so that contradicts that " + p_function('m') + " is false.\n"
    proof += "Conclusion: there is no n ∈ N where " + p_function('n') + " is false, so " + p_function('n') + " is true for every n ∈ N."
    return proof

def unroll(p_function, base_string, step_function, n):
    if n == 0:
        return base_string
    proof = base_string + "\n"
    for i in range(n):
        previous_step = f"{i} < 1 above" if i == 0 else f"a_{{{i}}} < 1 above"
        proof += p_function(str(i+1)) + ", since " + str(i+1) + " = " + str(i) + " + 1 and\n"
        proof += step_function(str(i), previous_step) + "\n"
    return proof




def compute_T(formula):
    # Base case: if the formula is a variable.
    if isinstance(formula, str) and formula.startswith('x_'):
        return formula
    
    # For the formula ¬p.
    if formula[0] == '¬':
        return ('¬', compute_T(formula[1]))
    
    # For the formulas p ∧ q.
    if formula[1] == '∧':
        # Two recursive calls on formulas of smaller size.
        return (compute_T(formula[0]), '∧', compute_T(formula[2]))
    
    if formula[1] == '∨':
        
        return (compute_T(formula[0]), '∨', compute_T(formula[2]))
    

# Example usage:
formula = (('x_1', '∧', ('¬', 'x_2')), '∨', 'x_3')
print(compute_T(formula))


