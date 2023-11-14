from app import app
from eventlet import wsgi, listen
import eventlet
eventlet.monkey_patch(socket=True, thread=False)

if __name__ == "__main__":
    wsgi.server(listen(("127.0.0.1", 5000)), app)
    #app.run()
