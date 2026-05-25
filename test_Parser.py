import pytest

from parsers import Parser


@pytest.fixture
def Parser_():
    url = 'https://www.google.com'
    return Parser(url)


def test_set_url(Parser_) -> None:
    """нет описания(еще не написал)"""
    with pytest.raises(ValueError):
        url = "google.com"
        parser = Parser(url)  # noqa: F841

    url = "https://google.com/"
    parser = Parser(url)
    assert parser.url == "https://google.com/"


def test_log(Parser_):
    parser = Parser(Parser_.url)
    parser.get_html(parser.url)
    assert parser.log == "(get_html) сработал: 10 раз(а) \n\x1b[34m(get_html) удачный ответ от сервера - '200' \n"
    # Parser_.get_html(Parser_.url)
    # assert Parser_.log == "\x1b[34m(get_html) удачный ответ от сервера - '200' \n\x1b[34m(get_html) удачный ответ от сервера - '200' \n"

if __name__ == "__main__":
    ...
