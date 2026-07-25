import time

import httpx
from bs4 import BeautifulSoup
from fastapi import HTTPException

REQUEST_TIMEOUT = 10.0


async def audit_website(url: str) -> dict:
    start_time = time.perf_counter()

    try:
        async with httpx.AsyncClient(
            follow_redirects=True,
            timeout=REQUEST_TIMEOUT,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/58.0.3029.110 Safari/537.3"
                )
            },
        ) as client:
            response = await client.get(url)

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="The request to the website timed out."
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail="Unable to connect to the requested website."
        )

    response_time_ms = round((time.perf_counter() - start_time) * 1000, 2)

    print("Final URL:", response.url)
    print("Status:", response.status_code)
    print("Content-Type:", response.headers.get("Content-Type"))
    print("Headers:", response.headers)

    content_type = response.headers.get("Content-Type", "").lower()

    if "text/html" not in content_type:
        raise HTTPException(
            status_code=415,
            detail="The requested URL does not return an HTML response."
        )

    soup = BeautifulSoup(response.text, "lxml")

    parsed = parse_html(soup)

    return {
        "url": str(response.url),
        "status": response.status_code,
        "response_time_ms": response_time_ms,
        **parsed,
    }


def parse_html(soup: BeautifulSoup) -> dict:
    return {
        "title": extract_title(soup),
        "meta_description": extract_meta_description(soup),
        "h1_count": count_h1(soup),
        "images_missing_alt": count_missing_alt(soup),
        "word_count": count_words(soup),
    }


def extract_title(soup: BeautifulSoup) -> str | None:
    if soup.title:
        title = soup.title.get_text(strip=True)
        return title if title else None
    return None


def extract_meta_description(soup: BeautifulSoup) -> str | None:
    meta = soup.find(
        "meta",
        attrs={
            "name": lambda value: value and value.lower() == "description"
        },
    )

    if not meta:
        return None

    content = meta.get("content", "").strip()

    return content if content else None


def count_h1(soup: BeautifulSoup) -> int:
    return len(soup.find_all("h1"))


def count_missing_alt(soup: BeautifulSoup) -> int:
    return len(
        [
            img
            for img in soup.find_all("img")
            if not img.get("alt")
        ]
    )


def count_words(soup: BeautifulSoup) -> int:
    temp_soup = BeautifulSoup(str(soup), "lxml")

    for tag in temp_soup(["script", "style", "noscript"]):
        tag.decompose()

    text = temp_soup.get_text(separator=" ", strip=True)

    return len(text.split())