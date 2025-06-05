import webbrowser


def search_google(query):
    url = f'https://www.google.com/search?q={query}'
    webbrowser.open(url)
    return f'Поиск Google: {query}'


if __name__ == '__main__':
    print(search_google('NOVA project'))
