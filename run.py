from app import create_app


appl = create_app()
appl.run(host=appl.config['HOST'], port=appl.config['PORT'])
