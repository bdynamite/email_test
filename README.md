# API для отправки Email

```
from email import Email

email = Email('test1@gmail.com', 'Hello gmail! I have an offer for you.')
email.send()
>>> {'email': "test1@gmail.com", 'Hello gmail!'}

email = Email('test2@yandex.ru', 'Hello yandex! I have an pic <img src="https://spam.org/pic1.png" /> for you.')
email.send()
>>> {'email': "test2@yandex.ru", 'Hello yandex! I have an pic https://spam.org/pic1.png for you.'}

email = Email('test3@mail.ru', 'Hello mail! I have an pic <img src="https://spam.org/pic1.gif" /> for you.')
email.send()
>>> {'email': 'test3@mail.ru', 'Hello mail! I have an pic <img src="https://spam.org/pic1.png" /> for you.'}

email = Email('test4@sailplay.ru', 'Hello another mail client! I have an offer for you.')
email.send()
>>> {'email': 'test4@sailplay.ru', 'Hello another mail client!'}
```

### Возможности:
1) Единая точка входа - Email()
2) Расширяемость на уровне правил фильтрации контента - добавление/изменение как самих функций фильтрации, так и порядка их применения к почтовому клиенту
3) Расширяемость на уровне почтовых клиентов - создание новых почтовых клиентов путем наследования от BaseMail и регистрация внутри Email