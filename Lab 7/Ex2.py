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

#c
evens = []

for num in range(2, 52, 2):
    evens.append(num)

print(evens)