
def a(*args):
    print(type(args))
    for arg in args:
        print(arg)

def b(**kwargs):
    print(type(kwargs))
    for key,value in kwargs.items():
        print(key,'  ',value)

list_a = [1,2,3]

e = {'a':1, 'b':2, 'c':3}

a(*list_a)
b(**e)





