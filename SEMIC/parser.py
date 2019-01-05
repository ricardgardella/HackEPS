import requests
import wikipedia
import hashlib

WEBSITE = 'https://en.wikipedia.org/wiki/WALL%C2%B7E'

def brute_force():
    page = requests.get(WEBSITE)
    page = wikipedia.page('1995')
    #text = page.text
    text = page.content
    words = text.split(' ')
    print('Analyzing {} words'.format(len(words)))
    for word in words:
        word = word.replace('.', '').replace(',', '')
        sha = hashlib.sha1()
        sha.update(word.encode('utf-8'))
        if sha.hexdigest() == "b8e46064c5cb98321ab378f546d2641881b43563":
            print('Match found. Password: ' + word)
            return True
    return False




if __name__ == '__main__':
    if not brute_force():
        print('Not found')