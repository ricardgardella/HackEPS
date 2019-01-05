from functools import reduce
from html.parser import HTMLParser

with open('sample.html', mode='r') as f:
    html = f.read()


class Errors:
    def __init__(self):
        self.errors = {}

    def add_error(self, index, code):
        if index not in self.errors:
            self.errors[index] = []
        self.errors[index].append(code)

    def print_errors_sorted(self):
        errors_list = list(self.errors.items())
        errors_list.sort(key=lambda e: e[0])
        for line, errs in errors_list:
            print(str(line) + ' : ' + reduce(lambda acc, x: acc + str(x), errs, ''))


class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def top(self):
        return self.items[len(self.items) - 1]


class Parser(HTMLParser):
    def handle_starttag(self, tag, attributes):
        stack.push(tag)

    def handle_endtag(self, tag):
        top = stack.top()
        if top == tag:
            print('= ', top, tag)
            stack.pop()
        else:
            print('!= ', top, tag)
            errors.add_error(self.getpos()[0], 1)

    def handle_comment(self, data):
        pass

    def error(self, message):
        pass


errors = Errors()
stack = Stack()
parser = Parser()
parser.feed(html)
parser.close()
errors.print_errors_sorted()
