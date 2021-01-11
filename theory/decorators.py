def df(original):
    def wrapper(*args,**kwargs): # args and kwargs is for any number of arguments and keyword argument
        print('a',*args)
        print('k', **kwargs)
        return original(*args,**kwargs)
    return wrapper
@df # same as saying display = df(display), which is also = wrapper
def display(x):
    print(x)

# display(1)

response = ['Go get Jason a cup of water','Go massage for Jason','Go keep your toys',"Go wash Jason's plate",'Go clean the table','I love you']

response1 = ['stupid','tiffany is fat','you are fat',"you're ugly","you're short and fat","you look like a fat pig"]
