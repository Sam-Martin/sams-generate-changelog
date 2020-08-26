class a:

    def __init__(self, a):
        self.a = a
    
    def __getattr__(self, attr):
        return 'GET ATTR'

class b(a):

    def __init__(self, b):
        super().__init__(b)
        self.b = b

B = b('hello')
print(B.a)
print(B.b)
print(B.c)