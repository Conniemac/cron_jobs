import io
import re
import smtplib
import ssl
from subprocess import Popen, PIPE
from email.message import EmailMessage


sender_email = "auto.grow.alerter.bot9431@gmail.com"
sender_password = "HisM4k39Vccshwn484jGEvagl"
receiving_emails = ["9785142966@vtext.com"]


def send_email_alert(alert_message: str):

	ssl_port = 465  # For SSL

	# Create a secure SSL context
	context = ssl.create_default_context()

	with smtplib.SMTP_SSL("smtp.gmail.com", ssl_port, context=context) as server:
		server.login(sender_email, sender_password)

		for email in receiving_emails:
			message_body = alert_message

			receiver_email = email

			email_message = EmailMessage()
			email_message.set_content(message_body)
			email_message['Subject'] = f'FATAL'
			email_message['From'] = sender_email
			email_message['To'] = receiver_email

			server.send_message(email_message)


def execute_command(command: list):

	subprocess = Popen(command, stdout=PIPE)
	result = subprocess.stdout

	with io.BufferedReader(result) as result_file:
		running_processes = [re.sub(" +", " ", line.decode("utf-8")) for line in result_file]

	return running_processes


def main():

	processes_to_find = {"system_is_up": {"process_name": "python3 framework_controller.py", "email_message": "!!!!!Auto-Grow is down. Restart immediately!!!!!"}}

	# Get a list of the processes that are currently running
	get_current_processes = ["ps", "aux"]
	running_processes = execute_command(get_current_processes)

	# Go through each of the running processes and check if framework controller is still running
	for key in processes_to_find.keys():

		target_process_is_running = False
		for process in running_processes:

			if process.find(processes_to_find[key]["process_name"]) > -1:
				target_process_is_running = True
				break

		# If the process is not running then send an alert
		if not target_process_is_running:
			send_email_alert(processes_to_find[key]["email_message"])


if __name__ == "__main__":
	main()