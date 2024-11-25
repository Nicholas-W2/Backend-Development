import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

def send_simple_message():
  	return requests.post(
  		"https://api.mailgun.net/v3/sandbox743a43737b574f668a61ed28c4706584.mailgun.org/messages",
  		auth=("api", "2ac6de5885598ed1c7e7f9f6494be7dc-c02fd0ba-cbd50aa9"),
  		data={"from": "Excited User <mailgun@sandbox743a43737b574f668a61ed28c4706584.mailgun.org>",
  			"to": ["nicholas.dw@atriauniversity.edu.in"],
  			"subject": "Hello",
  			"text": "Dear Varsha, We have noticed unusual activity or a potential compromise related to your Mailgun.org account. To protect your security, please do not share your password or sensitive details via email. To secure your account, we recommend: Resetting your password immediately via Mailgun's password reset page. Reviewing your account activity for any unauthorized access. If you need further assistance, please contact Mailgun support directly at support@mailgun.com. Thank you for your prompt attention to this matter. Best regards, Maria, Mailgun Support Team!"})

send_simple_message()

@app.route('/', methods=['POST'])
def index():
	send_simple_message()
	return "Email sent!"

@app.route('/webhook', methods=['POST'])
def webhook():
	print("Webhook received")
	data = request.get_json()
	print(data)
	return jsonify({"message":"OK"})

if __name__ == '__main__':
	app.run(debug=True)