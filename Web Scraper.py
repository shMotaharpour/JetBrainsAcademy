from pathlib import Path
from string import punctuation

import requests
from bs4 import BeautifulSoup

translate_dict = str.maketrans(' ', '_', punctuation)


def tag_leading_to_view_article(tag):
    return tag.has_attr("data-track-action") and tag["data-track-action"] == "view article"


def tag_containing_article_type(tag):
    return tag.name == "span" and tag.has_attr("data-test") and tag["data-test"] == "article.type"


def tag_containing_article_title(tag):
    return tag.name == "h1" and ("article" in tag["class"][0] and "title" in tag["class"][0])


def tag_containing_article_body(tag):
    return tag.name == "div" and ("article" in tag.get("class", [""])[0] and "body" in tag.get("class", [""])[0])


def get_article_links_of_type(url, article_type="News"):
    origin_url = 'https://www.nature.com'
    articles_resp = requests.get(url)
    soup = BeautifulSoup(articles_resp.text, "html.parser")
    articles = soup.find_all(tag_containing_article_type)
    articles = list(filter(lambda x: x.text.strip() == article_type, articles))
    return [origin_url + x.find_parent("article").find(tag_leading_to_view_article).get("href") for x in articles]


def get_article_title_and_content(url):
    article = requests.get(url)
    soup = BeautifulSoup(article.text, "html.parser")
    title = soup.find(tag_containing_article_title)
    content = soup.find(tag_containing_article_body)
    if title and content:
        return title.text.strip(), content.text.strip()


def get_articles_of_type_in_first_n_pages(n_pages, article_type):
    for i in range(1, n_pages + 1):
        dir_name = Path.cwd() / f"Page_{i}"
        dir_name.mkdir(parents=True, exist_ok=True)
        url = 'https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page=' + str(i)
        article_links = get_article_links_of_type(url, article_type=article_type)
        if article_links:
            for article_link in article_links:
                title, content = get_article_title_and_content(article_link)
                content = content.strip()
                title = f"{title.translate(translate_dict)}.txt"
                file_dir = dir_name / title
                with open(file_dir, "w", encoding='utf-8') as f:
                    f.write(content)


if __name__ == '__main__':
    pages_number = int(input())
    articles_type = input()
    get_articles_of_type_in_first_n_pages(pages_number, articles_type)
    print('All Articles saved')
