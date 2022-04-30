from aituNetwork import create_app
from dotenv import load_dotenv
from os import getenv

load_dotenv()


def main():
    app = create_app()

    host = getenv('HOST')
    port = getenv('PORT')

    if None in [host, port]:
        print('Host or port was not set.')
        exit()

    app.run(host=host, port=port)


if __name__ == '__main__':
    main()
