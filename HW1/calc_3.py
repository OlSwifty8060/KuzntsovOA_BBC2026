while True:
    a = int(input("Введите первое значение:"))
    b = int(input("Введите второе значение:"))
    c = str(input("Введите знак переменной:"))


    def P( a,  b,  c):
        if c == '+':
            return a + b
        
        if c == '-':
            return a - b

        if c == '/':
            return a / b

        if c == '*':
            return a * b

        
    print(P(a, b, c))

