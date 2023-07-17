from bs4 import BeautifulSoup


def fix_table_wrapping(infile_name: str,
                       outfile_name: str):
    with open(infile_name, 'r') as file:
        html_string = file.read()
    soup = BeautifulSoup(html_string, 'html.parser')

    for p_tag in soup.find_all('p'):
        if p_tag.find('table'):
            p_tag.replace_with_children()

    with open(outfile_name, 'w') as file:
        file.write(str(soup))


if __name__ == '__main__':
    # data/section/기타지원.html data/section/노령층지원.html data/section/법률금융복지지원.html data/section/보건의료지원.html data/section/보훈대상자지원.html data/section/생계지원.html data/section/임신보육지원.html data/section/장애인지원.html data/section/청소년청년지원.html data/section/취업지원.html
    fix_table_wrapping(infile_name="data/cleansed/기타지원.html",
                       outfile_name="data/fixed/기타지원.html",)
    fix_table_wrapping(infile_name="data/cleansed/노령층지원.html",
                       outfile_name="data/fixed/노령층지원.html",)
    fix_table_wrapping(infile_name="data/cleansed/법률금융복지지원.html",
                       outfile_name="data/fixed/법률금융복지지원.html",)
    fix_table_wrapping(infile_name="data/cleansed/보건의료지원.html",
                       outfile_name="data/fixed/보건의료지원.html",)
    fix_table_wrapping(infile_name="data/cleansed/보훈대상자지원.html",
                       outfile_name="data/fixed/보훈대상자지원.html",)
    fix_table_wrapping(infile_name="data/cleansed/생계지원.html",
                       outfile_name="data/fixed/생계지원.html",)
    fix_table_wrapping(infile_name="data/cleansed/장애인지원.html",
                       outfile_name="data/fixed/장애인지원.html",)
    fix_table_wrapping(infile_name="data/cleansed/청소년청년지원.html",
                       outfile_name="data/fixed/청소년청년지원.html",)
    fix_table_wrapping(infile_name="data/cleansed/취업지원.html",
                       outfile_name="data/fixed/취업지원.html",)
    fix_table_wrapping(infile_name="data/cleansed/임신보육지원.html",
                       outfile_name="data/fixed/임신보육지원.html",)
