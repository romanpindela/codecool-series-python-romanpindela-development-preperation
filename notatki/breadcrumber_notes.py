path = "/tv-show/1409".split('/')
print(path)

for item in path[1:]:
    index_item=path.index(item)
    print(index_item)
    if item != path[-1]:
        print(item)

        print('/'+'/'.join(path[1:(index_item+1)]))
    else:
        print(item)
        print('/'+'/'.join(path[1:(index_item+1)]))


https://www.programiz.com/python-programming/online-compiler/
output:
Hello world
['', 'tv-show', '1409']
1
tv-show
/tv-show
2
1409
/tv-show/1409
> 

