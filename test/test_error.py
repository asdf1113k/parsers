class Set(set):
    def __getitem__(self, index: int) -> list:
        return list(self)[index]        