"""if (int(people[4]) - int(people[3])) != (int(people[5]) - int(people[4])):
    print('ok')
else:
    print('pass')"""
#print(people[6])
#print(int(people[7]) - int(people[6]))

"""last = []
for i in range(len(people) - 2):
    if (int(people[i+1]) - int(people[i])) != (int(people[i+2]) - int(people[i+1])):
        last.append(i)
    else:
        pass

print(last)"""

# 5, 8, 9, 10, 11, 12, 15, 16, 17, 18, 19
people = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6:'8', 7: '9', 8: '10', 9: '11', 10: '12', 11: '15'}

"""last = []
for i in range(len(people) - 1):
    if (int(people[i+1]) - int(people[i])) > 1:
        last.append(i)
    else:
        pass
"""

last = [0, 1, 2]
for idx in range(len(people)):
    if idx not in last:
        del people[idx]

print(last)
print(people)