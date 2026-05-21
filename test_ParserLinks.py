import pytest

from ParserLinks import Parser


def test_ParserLinks():
    url = "https://google.com/"
    parser = Parser(url)

    with pytest.raises(ValueError, match="URL должен оканчиватся на '/' "):
        parser.get_html(url[0:-1]) # "https://google.com"

    assert type(parser.links) is set  # assert переводится как утверждать
