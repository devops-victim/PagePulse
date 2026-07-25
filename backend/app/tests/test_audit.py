from bs4 import BeautifulSoup

from app.services.audit import (
    extract_title,
    extract_meta_description,
    count_h1,
    count_missing_alt,
    count_words,
    parse_html,
)


def make_soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "lxml")


def test_extract_title():
    soup = make_soup("""
    <html>
        <head>
            <title>My Website</title>
        </head>
    </html>
    """)

    assert extract_title(soup) == "My Website"


def test_extract_title_none():
    soup = make_soup("<html></html>")

    assert extract_title(soup) is None


def test_extract_meta_description():
    soup = make_soup("""
    <meta
        name="description"
        content="This is a demo website."
    >
    """)

    assert extract_meta_description(soup) == "This is a demo website."


def test_extract_meta_description_none():
    soup = make_soup("<html></html>")

    assert extract_meta_description(soup) is None


def test_extract_meta_description_case_insensitive():
    soup = make_soup("""
    <meta
        NAME="DESCRIPTION"
        content="SEO Description"
    >
    """)

    assert extract_meta_description(soup) == "SEO Description"


def test_count_h1():
    soup = make_soup("""
    <h1>One</h1>
    <h1>Two</h1>
    <h2>Ignored</h2>
    """)

    assert count_h1(soup) == 2


def test_count_missing_alt():
    soup = make_soup("""
    <img src="1.png">
    <img src="2.png" alt="">
    <img src="3.png" alt="Logo">
    """)

    assert count_missing_alt(soup) == 2


def test_count_words():
    soup = make_soup("""
    <html>
        <body>

            Hello world.

            <script>
                var x = 10;
            </script>

            <style>
                body{color:red;}
            </style>

            FastAPI is awesome.

        </body>
    </html>
    """)

    assert count_words(soup) == 5
    # Hello world FastAPI is awesome


def test_parse_html():
    soup = make_soup("""
    <html>

        <head>
            <title>Test Site</title>

            <meta
                name="description"
                content="Testing parser"
            >
        </head>

        <body>

            <h1>Heading</h1>

            <img src="a.png">

            <img
                src="b.png"
                alt="Logo"
            >

            Hello from parser.

        </body>

    </html>
    """)

    result = parse_html(soup)

    assert result["title"] == "Test Site"
    assert result["meta_description"] == "Testing parser"
    assert result["h1_count"] == 1
    assert result["images_missing_alt"] == 1
    assert result["word_count"] == 6