list_ = [
    {'j': 5, 'g': 6, 'w': 8, 'q': 3},
    {'j': 5, 'g': 0, 'w': 8, 'q': 3},
    {'j': 5, 'g': 6, 'w': 8, 'q': 3},
    {'j': 5, 'g': 6, 'w': 8, 'q': 3}
]

for i in list_:
    if 0 in i.values(): list_.pop(list_.index(i))
print(list_)
