from os import getenv

from aituNetwork import create_app


app = create_app()


def main():
    host = getenv('HOST')
    port = getenv('PORT')
    debug = getenv('DEBUG')

    if None in [host, port, debug]:
        print('Host, port or debug values was not set.')
        exit()

    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    main()
