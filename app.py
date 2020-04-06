from app import start_app


if __name__ == '__main__':
    app = start_app()
    app.run(host=app.config['HOST'], port=app.config['PORT'])
