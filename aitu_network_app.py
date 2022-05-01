from flask_migrate import Migrate

from aituNetwork import create_app, db
from os import getenv


app = create_app()
migrate = Migrate(app, db)


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
