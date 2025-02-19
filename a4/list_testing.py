import time

start = time.time()
new_list = [[1,  2,  3,  4],
            [5,  6,  7,  8],
            [9, 10, 11, 12]]
diags = []
h = len(new_list)
l = len(new_list[0])

for i in range(-l,h):
    diag = []

    for j in range(l):

        if i+j<h and i+j>=0:
            index = (i+j,j)
        else:
            continue
        diag.append(new_list[index[0]][index[1]])
    if diag:
        diags.append(diag)

diags2 = []


end = time.time()

print(diags)
print((end - start)*10**3)

