
name = "13 Дудинка ТЦ Океан"
name = name.split()
n1 = name[0]
n2 = ' '.join(name[1:])
n = 4 - len(n1)
if n == 1:
    n1 = f"{n1} "
elif n == 2:
    n1 = f"{n1}  "
elif n == 3:
    n1 = f"{n1}   "
name = f"{n1} {n2}"
print(name)
