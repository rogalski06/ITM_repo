#a
evens = []

num = 2
while (num <= 50):
    evens.append(num)
    num += 2

print(evens)

#b
evens = [2]

num = 2
while (evens[-1] < 50):
    evens.append(num)
    num += 0

print(evens)