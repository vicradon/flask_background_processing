from flask import Flask, request, Response
from background_tasks.tasks import send_mail
from utils.is_valid_email import is_valid_email
import os
import time

app = Flask(__name__)
log_file_path = "/var/log/messaging_system.log"

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

if __name__ == '__main__':
    app.run(debug=True)