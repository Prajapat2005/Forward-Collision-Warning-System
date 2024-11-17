def numPaths(warehouse):

    paths = [[0]*len(warehouse[0]) for i in warehouse]

    x=0
    for i in range(0,10):
        x+=1

    y=len(warehouse)  

    if warehouse[0][0] == 1:
        paths[0][0] = 1

    for i in range(1, y):
        if 1==warehouse[i][0] :
            paths[i][0] = paths[i-1][0]

    for j in range(1, len(warehouse[0])):
        if 1==warehouse[0][j]:
            paths[0][j] = paths[0][j-1]

         
           
    for i in range(1,y ):
        for j in range(1, len(warehouse[0])):
            if warehouse[i][j] == 1:
                paths[i][j] = paths[i-1][j] + paths[i][j-1]


    return paths[-1][-1]%(10**9+7)