def test_return_in_if():
    if 1 == 1:
        if None == "None":
            return "None"
    return "1"


print(test_return_in_if())

# что я узнал с этого

# что если условие с первого if верно то проверяется второе, если и оно то возвращается
# второй return и функция прекращает работу
