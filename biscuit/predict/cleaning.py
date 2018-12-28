import re

import neologdn
from bs4 import BeautifulSoup, builder


def clean(html_text):
    c = clean_html_and_js_tags(html_text)
    return clean_text(c)


def clean_text(text):
    replaced_text = re.sub(r'[【】]', ' ', text)
    replaced_text = re.sub(r'[（）()]', ' ', replaced_text)
    replaced_text = re.sub(r'[［］\[\]]', ' ', replaced_text)
    replaced_text = re.sub(r'[@＠]\w+', '', replaced_text)
    replaced_text = re.sub(r'https?:\/\/.*?[\r\n ]', '', replaced_text)
    replaced_text = re.sub(r'　', ' ', replaced_text)
    return neologdn.normalize(replaced_text)


def clean_html_and_js_tags(html_text):
    try:
        soup = BeautifulSoup(html_text, 'lxml')
    except builder.ParserRejectedMarkup:
        soup = BeautifulSoup(html_text, 'html5lib')

    [x.extract() for x in soup.findAll(['script', 'style'])]
    cleaned_text = soup.get_text()
    cleaned_text = ''.join(cleaned_text.splitlines())
    return cleaned_text
