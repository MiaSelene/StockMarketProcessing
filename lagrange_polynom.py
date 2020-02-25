def lagrange(x, y):
    """takes two lists x and y and returns a polynomial f, with f(xi) = yi"""
    polynomials = []

    for i in range(len(x)):
        fi = ['1']
        for xk in x[:i]+x[i+1:]:
            fi = multiply(fi, ['x', str(-xk)])
        fi = multiply(fi, [str(y[i]/evaluate(fi,x[i]))])
        polynomials.append(fi)
    return polynomial_sum(polynomials)

def multiply(a, b):
    """takes to lists of terms a = (a1 + a2 + ... + an) and b = (b1 + b2 + ... + b3) and performs a * b"""
    """not that preceding numbers are handled as factors and appended numbers as indeces"""
    res = {}
    for term_a in a:
        base_a, factor_a = extract_factor(term_a)
        for term_b in b:
            base_b, factor_b = extract_factor(term_b)
            factor_c = float(factor_a) * float(factor_b)
            if factor_c == 1:
                factor_c == ''
            polarity = 1 if (base_a.count('-') + base_b.count('-'))%2 == 0 else -1
            base = base_a.replace('-','') + base_b.replace('-','')
            if base in res.keys():
                res[base] += factor_c * polarity
            else:
                res[base] = polarity * factor_c
    new = []
    for key in res.keys():
        new.append(str(res[key]) + key)
    return new

def extract_factor(term):
    for i in range(len(term)):
        if not term[i].isdigit() and term[i] != '.' and term[i] != '-':
            if term[:i] == '':
                return term[i:], '1'
            return term[i:], term[:i]
    return '', term

def evaluate(pol, x):
    new = 0
    for term in pol:
        base, factor = extract_factor(term)
        new += float(factor) * x**base.count('x')
    return new


def polynomial_sum(polynomials):
    res = {}
    display = ''
    for pol in polynomials:
        for term in pol:
            base, factor = extract_factor(term)
            if base in res.keys():
                res[base] += float(factor)
            else:
                res[base] = float(factor)
    for key in res.keys():
        display += str(res[key]) + 'x^' + str(key.count('x')) + '+'

    return display[:-1]

if __name__ == '__main__':
    print(lagrange([1,2,3], [1,-1,-2]))
