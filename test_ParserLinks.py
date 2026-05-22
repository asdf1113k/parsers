import pytest

from ParserLinks import Parser


@pytest.fixture
def test_Parser() -> Parser:
    url = "https://google.com/"
    return Parser(url)

def test_set_url() -> None:
    
    with pytest.raises(ValueError):
        url = "google.com"
        parser = Parser(url)  # noqa: F841
    # проверка на назначение url
    url = "https://google.com/"
    parser = Parser(url)
    assert parser.url == "https://google.com/"
    
        

def test_get_html(test_Parser) -> None:
    
    # сделать автоматическое добавлнение "/" в конце url
    # сделать отдельный метод для этого запускающиеся в __init__

    assert type(test_Parser.links) is list  # assert переводится как утверждать
    test_Parser.get_html(test_Parser.url)
    assert test_Parser.count_get_html == 1
    assert len(test_Parser.cheaking_links) == 1
    assert test_Parser.cheaking_links == {"https://www.google.com/"}

    


def test_set_auto_run(test_Parser) -> None:
    with pytest.raises(ValueError):
        test_Parser.set_auto_run(1)
    with pytest.raises(ValueError):
        test_Parser.set_auto_run("False")
    
    test_Parser.set_auto_run(True)
    assert test_Parser.auto_run == True
    test_Parser.set_auto_run(False)
    assert test_Parser.auto_run == False


    

if __name__ == "__main__":
    print("https://google.com/"[0:8])