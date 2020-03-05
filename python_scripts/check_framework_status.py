import io
import re
import smtplib
import ssl
from subprocess import Popen, PIPE
from email.message import EmailMessage


sender_email = "auto.grow.alerter.bot9431@gmail.com"
sender_password = "HisM4k39Vccshwn484jGEvagl"
receiving_emails = ["9785142966@vtext.com"]


def send_email_alert():

	ssl_port = 465  # For SSL

	# Create a secure SSL context
	context = ssl.create_default_context()

	with smtplib.SMTP_SSL("smtp.gmail.com", ssl_port, context=context) as server:
		server.login(sender_email, sender_password)

		for email in receiving_emails:
			message_body = "!!!!Auto-Grow is down. Restart ASAP!!!!"

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

	target_process_name = "python3 framework_controller.py"

	# Get a list of the processes that are currently running
	get_current_processes = ["ps", "aux"]
	running_processes = execute_command(get_current_processes)

	# Go through each of the running processes and check if framework controller is still running
	target_process_is_running = False
	for process in running_processes:

		process_name = process.split(" ")[10]
		print(process_name)
		if process_name == target_process_name:
			target_process_is_running = True
			break

	# If the process is not running then send an alert
	if not target_process_is_running:
		send_email_alert()


if __name__ == "__main__":
	main()