from app import create_app

if __name__ == '__main__':
    appl = create_app()
    appl.run(host=appl.config['HOST'], port=appl.config['PORT'])
