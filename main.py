import requests
from bs4 import BeautifulSoup

PAGES_TO_CRAWL = 3
MIN_SCORE = 100


def get_page(page_num):
    res = requests.get('https://news.ycombinator.com/news?p=' + str(page_num))
    return BeautifulSoup(res.text, 'html.parser')


def get_pages(pages_to_crawl=PAGES_TO_CRAWL):
    return [get_page(page_num + 1) for page_num in range(pages_to_crawl)]


def get_scores(stats):
    scores = []
    for row in stats:
        score_result = row.select('.score')
        score = int(score_result[0].getText()[:-7]) if score_result != [] else 0
        scores.append(score)
    return scores


def get_posts(*args):
    titles = []
    links = []
    scores = []
    for page in args:
        title_links = page.select('.titlelink')
        titles.extend([title_link.getText() for title_link in title_links])
        links.extend([title_link.get('href', None) for title_link in title_links])
        scores.extend(get_scores(page.select('.subtext')))
    return [{'title': titles[i], 'link': links[i], 'score': scores[i]} for i in range(len(scores))]


def print_posts(posts, min_score=MIN_SCORE):
    for post in sorted(posts, key=lambda k: k['score'], reverse=True):
        if post['score'] >= min_score:
            print(f"{post['title']} - {post['score']} votes")
            print(post['link'], end='\n\n')
        else:
            break


def main():
    pages = get_pages()
    posts = get_posts(*pages)
    print_posts(posts)


if __name__ == '__main__':
    main()