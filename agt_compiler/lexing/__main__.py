if __name__ == '__main__':
    import sys
    from . import get_tokens
    data = open(sys.argv[1]).read()
    for t in get_tokens(data):
        print(t)
