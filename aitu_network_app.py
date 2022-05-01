from aituNetwork import create_app
from dotenv import load_dotenv
from os import getenv

load_dotenv()


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
