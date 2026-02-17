#1a
nums = []

for num in range(1, 51):
    if num % 2 == 1:
        nums.append(num)

print(nums)

#1b
for num in range (0,25):
    odd_value = 2*num + 1
    if odd_value < 50:
        print(odd_value)

#1c
for num in range(1, 51, 2):
    print(num)