from IncendiosForestales import app 

if __name__ == "__main__":
  from gunicorn.app.wsgiapp import WSGIApplication
  application = WSGIApplication()
  application.wsgi_app = app
  application.run()
