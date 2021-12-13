# sends a request to flask api
# gets the list of emails and preferences
# scraps the website accordingly
# From AWS Lambda, sends back an email with a table of the prices of investment funds on a daily basis to registered users.

import requests
import os
from fon_handler import Fon
import json
import smtplib
from email.message import EmailMessage
from jinja2 import Template


def lambda_handler(event, context):
	# sends a request to api to get user emails and preferences
	response = requests.get('https://fonbulteni.herokuapp.com/jsoner', auth=('mailer', os.environ['REQ_PASS']))
	json_data = json.loads(response.text)

	prices = {}
	prices_to_db = {}
	for key in json_data:
		prices[key] = []
		for item in json_data[key]:
			fund = Fon(item)
			price = fund.get_price()
			name = fund.get_name()
			change = fund.daily_change()
			prices[key].append((name, price, change, item))
			prices_to_db[item] = [price, change]



	mail_addresses = [i for i in prices.keys()]
	subject = 'Fon Bulteni'

	email_user = os.environ['MAIL_USER']
	email_pass = os.environ['MAIL_PASS']

	body = 'Fonlarınızın Bugünkü Performansları'

	# used a jinja template for dynamically creating html mails for each user

	with open('mailer.html', 'r') as f:
		content = f.read()

	template = Template(content)

	for address in mail_addresses:
		table_data = prices[address]
		content_html= template.render(table_data=table_data)

		msg = EmailMessage()
		msg['Subject'] = subject
		msg['From'] = email_user
		msg['To'] = address
		msg.set_content(body)
		msg.add_alternative(content_html, subtype="html")

		with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
		     smtp.login(email_user, email_pass)
		     smtp.send_message(msg)

	put_req = requests.put('https://fonbulteni.herokuapp.com/jsoner', json=prices_to_db, auth=('mailer', os.environ['REQ_PASS']))

	print(put_req.text)





