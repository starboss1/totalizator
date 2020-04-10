from app import app

if __name__ == '__main__':
    print(app)
    app.run(host=app.config['HOST'], port=app.config['PORT'])
