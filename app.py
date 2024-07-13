from flask import Flask, request, render_template, send_file, Response
from flask_socketio import SocketIO
from background_tasks.tasks import send_mail
from utils.is_valid_email import is_valid_email
import threading
import time
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SOCKET_SECRET")
# socketio = SocketIO(app, cors_allowed_origins="*.ngrok-free.app, http://localhost:*")
socketio = SocketIO(app, cors_allowed_origins="*")
log_file_path = "/var/log/messaging_system.log"
log_tailing_active = threading.Event()

@app.route('/')
def handle_endpoints():
    query_params = list(request.args.keys())
    email_address = request.args.get('sendmail')
    error_msg = "No appropriate query parameter provided, only use one of ?sendmail='an email address' or ?talktome"

    if not query_params:
        return error_msg

    first_query_param = query_params[0]

    if first_query_param == "sendmail":
        if is_valid_email(email_address):
            send_mail.delay(email_address)
            return "Email queued for sending"

        return "Email address not valid"
    elif first_query_param == "talktome":
        return talktome()
    else:
        return error_msg

def talktome():
    with open(log_file_path, "a") as logfile:
        localtime = time.localtime()
        localtime_str = time.strftime("%H:%M:%S", localtime)
        logfile.write(localtime_str + "\n")


    return f"current time {localtime_str}, logged successfully"


def tail_log():
    log_tailing_active.set()

    with open(log_file_path, 'r') as f:
        f.seek(0, os.SEEK_END)
        while log_tailing_active.is_set():
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            socketio.emit('logs_update', {'data': line}, namespace="/logs")

def read_all_logs():
    with open(log_file_path, 'r') as f:
        return f.read()
    
@app.route('/logs', methods=['GET'])
def start_log_tailing():
    try:
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as log_file:
                logs = log_file.read()
            return Response(logs, mimetype='text/plain')
        else:
            return "Log file not found.", 404
    except Exception as e:
        return str(e), 500

    # user_agent = request.headers.get('User-Agent')
    # if 'Mozilla' not in user_agent:
    #     return send_file(log_file_path, as_attachment=True)
    
    # else:
    #     if not log_tailing_active.is_set():
    #         socketio.start_background_task(tail_log)
    #     return render_template('logs.html')

@socketio.on('connect', namespace='/logs')
def handle_connect():
    print("Client connected")
    initial_logs = read_all_logs()
    socketio.emit('initial_logs', {'data': initial_logs}, namespace="/logs")

@socketio.on('disconnect', namespace='/logs')
def handle_disconnect():
    print("Client disconnected")
    log_tailing_active.clear()

if __name__ == '__main__':
    socketio.run(app, debug=True)