colection = {None, 1, 1, 1, 2, 3, 3}  # в этом set нам не нужен None

print(colection)
colection.discard(None)  # удаляем
print(colection)

# как обращася к элементам set?
# нечего лучше не придумал
list(colection)[0]
# или 
class Set(set):
    def __getitem__(self, index: int) -> list:
        return list(self)[index]


colection = Set(["text", 1, 1, 1, 2, 3, 3])

print(colection)
print(colection[0])
