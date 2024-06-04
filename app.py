#! /usr/bin/env python
import json, os, sys
import stripe

from flask import Flask, render_template, jsonify, request, send_from_directory
from dotenv import load_dotenv, find_dotenv

# Load and parse the .env file before proceeding
dotenv_error = """A '.env' file was not found or did not contain the required keys as:
STRIPE_SECRET_KEY=<your-secret-key>
STRIPE_PUBLISHABLE_KEY=<your-publishable-key>
Please ensure that the file exists with the correct information.
The Stripe secret and publishable keys are available from the API tab in
your Stripe dashboard: https://dashboard.stripe.com/apikeys"""

try:
  load_dotenv(find_dotenv())
  stripe_keys = {
      "secret_key": os.environ["STRIPE_SECRET_KEY"],
      "publishable_key": os.environ["STRIPE_PUBLISHABLE_KEY"]
  }
except:
  sys.exit(dotenv_error)

# Setup the Stripe object correctly with customer information
stripe.api_key = stripe_keys["secret_key"]

# For sample support and debugging, not required for production:
stripe.set_app_info(
    'sa-takehome-project/jasper-aorangi',
    version='0.0.1',
    url='https://github.com/spmp/sa-takehome-project')

# We are going to use a global object here in place of a DB to hold sale state
item_state = {
    "title": None,
    "amount": 100
  }

# Setup the Flask App, including template directories etc.
app = Flask(__name__,
  static_url_path='',
  static_folder=os.path.join(
      os.path.dirname(os.path.abspath(__file__)), "public"),
  template_folder=os.path.join(
      os.path.dirname(os.path.abspath(__file__)), "views"))


# Config route to get the publishable key
@app.route('/config', methods=['GET'])
def get_config():
    return jsonify({'publishableKey': os.getenv('STRIPE_PUBLISHABLE_KEY')})

# 'Create payment intent' route to get the client ID
# This must be provided as a POST query such that the purchase price cannot
# be spoofed on a GET. In order to find the price some form of state is
# is required, and is provided by the 'item_state' variable.
@app.route("/create-payment-intent", methods=["POST"])
def create_payment_intent(currency='usd'):
  payment_intent = stripe.PaymentIntent.create(
    # Get the amount from the global state dict
    amount=item_state["amount"],
    currency=currency,
    automatic_payment_methods={'enabled': True}
  )
  return jsonify(clientSecret=payment_intent.client_secret)

# The root / route
@app.route('/', methods=['GET'])
def get_root():
    return render_template('index.html')

# The checkout route which contains the hardcoded middle weirdness
@app.route('/checkout', methods=['GET'])
def checkout():
# Hardcoding amounts here to avoid using a database
  item = request.args.get('item')
  item_state["title"] = None
  item_state["amount"] = None
  error = None

  if item == '1':
    item_state["title"] = 'The Art of Doing Science and Engineering'
    item_state["amount"] = 2300
  elif item == '2':
    item_state["title"] = 'The Making of Prince of Persia: Journals 1985-1993'
    item_state["amount"] = 2500
  elif item == '3':
    item_state["title"] = 'Working in Public: The Making and Maintenance of Open Source'
    item_state["amount"] = 2800
  else:
    # Included in layout view, feel free to assign error
    error = 'No item selected'

  return render_template('checkout.html',
    title=item_state["title"], amount=item_state["amount"], error=error)

# Success route
@app.route('/success', methods=['GET'])
def success():
  return render_template('success.html')

if __name__ == '__main__':
    app.run(port=4242, debug=True)
