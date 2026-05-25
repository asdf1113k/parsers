import pytest

from parsers import ParserLinks


@pytest.fixture
def class_ParserLinks() -> ParserLinks:
    url = "https://google.com/"
    return ParserLinks(url)





def test_get_html(class_ParserLinks) -> None:

    # сделать автоматическое добавлнение "/" в конце url
    # сделать отдельный метод для этого запускающиеся в __init__

    assert (
        type(class_ParserLinks.link_queue) is list
    )  # assert переводится как утверждать
    class_ParserLinks.get_html(class_ParserLinks.url)
    assert class_ParserLinks.count_get_html == 1
    assert len(class_ParserLinks.cheaking_links) == 1
    assert class_ParserLinks.cheaking_links == {"https://www.google.com/"}


def test_set_auto_run(class_ParserLinks) -> None:
    with pytest.raises(ValueError):
        class_ParserLinks.set_auto_run(1)
    with pytest.raises(ValueError):
        class_ParserLinks.set_auto_run("False")

    assert class_ParserLinks.set_auto_run(True) == True  # noqa: E712
    assert class_ParserLinks.auto_run == True  # noqa: E712
    assert class_ParserLinks.set_auto_run(False) == False  # noqa: E712
    assert class_ParserLinks.auto_run == False  # noqa: E712


def test_parsing_page():
    parser = ParserLinks("http://192.168.1.16:5500/www/", auto_run=True)


if __name__ == "__main__":
    # print("https://google.com/"[0:8])
    parser = ParserLinks(
        "http://192.168.1.16:5500/www/",
        auto_run=True,
    )
    # print(f"запросов сделано            : {parser.count_get_html}")
    # print(f"ссылок на очередь парсинга  : {len(parser.link_queue)}")
    # print(parser.link_queue)
    # print(f"спарсеные ссылки            : {len(parser.cheaking_links)}")
    # print(parser.cheaking_links)
