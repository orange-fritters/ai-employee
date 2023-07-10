from bs4 import BeautifulSoup, Tag, NavigableString


def has_subsection_style(tag):
    if tag.has_attr('style'):
        if 'overflow:hidden' in tag['style'] and 'width:635px' in tag['style']:
            return True
    return False


def has_article_style(tag):
    if tag.has_attr('style'):
        if 'font-size:12.0pt' in tag['style'] and 'font-weight:bold' in tag['style'] and 'text-decoration:underline' in tag['style']:
            return True
    return False


def cleanse(file_name: str):
    with open(file_name, "r") as file:
        content = file.read()
    soup = BeautifulSoup(content, 'html.parser')

    for tag in soup.find_all():
        content = tag.string
        if content is not None:
            content = content.strip()
            if content == '':
                tag.extract()

    for tag in soup.find_all(True, {'class': True}):
        if tag.name == "table" and tag.get('border') == '1':
            continue
        del tag['class']
        del tag['cellpadding']
        del tag['cellspacing']

    for tag in soup.find_all(True, {'bgcolor': True}):
        del tag['bgcolor']

    for tag in soup.find_all(True, {'valign': True}):
        del tag['valign']

    tags_with_target_style = soup.find_all(has_subsection_style)
    for i, tag in enumerate(tags_with_target_style, start=1):
        parent = tag.find_parent().find_parent()
        new_div = soup.new_tag('div')
        new_div['class'] = 'subsection'
        parent.replace_with(new_div)
        new_div.append(parent)

    for div in soup.find_all('div', {'class': 'subsection'}):
        div.parent.unwrap()

    subsections = soup.find_all('div', {'class': 'subsection'})
    for index, subsection in enumerate(subsections):
        elems = []
        next_subsection = subsections[index + 1] if index + 1 < len(subsections) else None

        for sibling in list(subsection.next_siblings):
            if sibling is next_subsection:
                break
            if isinstance(sibling, NavigableString):
                continue
            elems.append(sibling.extract())

        new_div = soup.new_tag('div')
        new_div['class'] = 'section'
        new_div.append(subsection.extract())

        for e in elems:
            new_div.append(e)

        soup.append(new_div)

    tags_with_article_style = soup.find_all(has_article_style)
    for article in tags_with_article_style:
        article.parent.unwrap()

    for section in soup.find_all('div', {'class': 'section'}):
        articles = section.find_all(has_article_style)
        for index, article in enumerate(articles):
            elems = []
            next_article = articles[index + 1] if index + 1 < len(articles) else None
            for sibling in list(article.next_siblings):
                if next_article is not None and sibling in next_article:
                    break
                if isinstance(sibling, NavigableString):
                    continue
                elems.append(sibling.extract())

            # Create new div and append all extracted elements to it
            new_div = soup.new_tag('div')  # Create a new div tag
            new_div['class'] = 'article'
            new_div.append(article.extract())

            for e in elems:
                new_div.append(e)

            section.append(new_div)

    for tag in soup.find_all(True, {'style': True}):
        del tag['style']

    for tag in soup.find_all('table'):
        tag['border'] = '1'

    for tag in soup.find_all('div', {'class': 'article'}):
        span = tag.find('span')
        if span is not None:
            span['style'] = 'font-weight:bold'

    soup.find('div').unwrap()

    for p in soup.find_all('p'):
        if len(p.contents) == 0:
            p.extract()

    for p in soup.find_all('p'):
        if len(p.contents) == 1:
            p.replace_with(p.contents[0])

    with open("file.html", "w") as file:
        file.write(str(soup.prettify()))


if __name__ == "__main__":
    cleanse("data/first.html")
