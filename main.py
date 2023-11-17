def in_array(array1, array2):
    arr = set()
    for i in array1:
        for j in array2:
            if i in j:
                arr.add(i)

    return [*arr]

a1 = ["tarp", "mice", "bull"]

a2 = ["lively", "alive", "harp", "sharp", "armstrong"]
print(in_array(a1, a2))