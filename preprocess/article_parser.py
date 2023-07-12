from bs4 import BeautifulSoup

html_files = ["기타지원.html", "노령층지원.html", "법률금융복지지원.html", "보건의료지원.html", "보훈대상자지원.html",
              "생계지원.html", "임신보육지원.html", "장애인지원.html", "청소년청년지원.html", "취업지원.html"]

for html_file in html_files:
    with open(f'data/fixed/{html_file}', 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    articles = soup.find_all('div', class_='article')

    for i, article in enumerate(articles, start=1):
        with open(f'data/articles/{html_file[:-5]}_{i}.html', 'w', encoding='utf-8') as file:
            file.write(str(article.prettify()))
