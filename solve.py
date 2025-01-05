import sympy as sp

# Define symbols
_x, _y = sp.symbols('_x _y')

# Define the equations
eq1 = sp.Eq(x[0][0]*_x + x[0][1]*_y + x[0][2]*_x*_y + x[0][3], now_x)
eq2 = sp.Eq(x[0][4]*_x + x[0][5]*_y + x[0][6]*_x*_y + x[0][7], now_y)

# Solve the equations
solution = sp.solve((eq1, eq2), (_x, _y))

print("Solution:")
print("_x =", solution[_x])
print("_y =", solution[_y])
