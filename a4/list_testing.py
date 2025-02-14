
new_list = [[1,  2,  3,  4],
            [5,  6,  7,  8],
            [9, 10, 11, 12]]
diags = []
h = len(new_list)
l = len(new_list[0])

for i in range(-l,h):
    diag = []
    for j in range(l):
        if i < 0:
            j = -i-1
            i = i + l - j

        if i < h and j < l:
            index = (i+j,j)
        else:
            break
        diag.append(new_list[index[0]][index[1]])
    diags.append(diag)

print(diags)
