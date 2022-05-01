from aituNetwork import create_app
from os import getenv


def main():
    app = create_app()

    host = getenv('HOST')
    port = getenv('PORT')
    debug = getenv('DEBUG')

    if None in [host, port, debug]:
        print('Host, port or debug values was not set.')
        exit()

    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    main()
