from functools import partial
import re


def filter_sentence_by_word(word, text):
    sentence_end_regex = re.compile(r'[\.\?!]+')
    result = []
    smth = 0
    start_sentence = 0
    for match in re.finditer(sentence_end_regex, text):
        sentence = text[start_sentence:match.end()]
        if word not in sentence:
            result.append(sentence)
        start_sentence = match.end()
    return ''.join(result)


def replace_img_tag_by_src(text):
    img_src_regex = re.compile(r'(<img .*?(?<=src=\")(.*?)(?=\").*?/>)')
    src_repl = r'\2'
    return re.sub(img_src_regex, src_repl, text)


def replace_img_gif_by_png(text):
    gif_regex = re.compile(r'.gif')
    png_repl = r'.png'
    return re.sub(gif_regex, png_repl, text)


class BaseMail:

    _api_url = None
    _content_filters = []

    def __init__(self, email, content):
        self.email = email
        self.original_content = content

    def send(self):
        content = self._filter_content()
    #     smth like requests.post(self._api_url, json={'email': self.email, 'content': content})
        return {'email': self.email, 'content': content}

    def _filter_content(self):
        content = self.original_content
        for filter_func in self._content_filters:
            content = filter_func(content)
        return content


class Gmail(BaseMail):

    _api_url = 'https://email-machine.internal/api/email-gate/gmail/'
    _content_filters = [
        partial(filter_sentence_by_word, 'offer'),
    ]


class Yandex(BaseMail):

    _api_url = 'https://email-machine.internal/api/email-gate/yandex/'
    _content_filters = [
        replace_img_tag_by_src,
    ]


class Mail(BaseMail):

    _api_url = 'https://email-machine.internal/api/email-gate/mail/'
    _content_filters = [
        replace_img_gif_by_png,
    ]


class Email:

    _domains = {
        'gmail': Gmail,
        'yandex': Yandex,
        'mail': Mail,
    }
    _domain_regex = re.compile(r'(?<=@).*?(?=\.)')

    def __new__(cls, email: str, content: str):
        email_domain = re.search(cls._domain_regex, email)
        if email_domain is None:
            raise ValueError(f'cannot extract domain from email {email}')
        domain_cls = cls._domains.get(email_domain.group(0), Gmail)
        return domain_cls(email, content)
