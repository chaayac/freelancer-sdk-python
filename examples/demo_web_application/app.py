from flask import Flask, redirect, request, jsonify, render_template, session
from models import db, User
from functools import wraps
import requests
import json
from freelancersdk.session import Session
from freelancersdk.resources.projects.types import MilestoneReason
from freelancersdk.resources.projects import (
    create_local_project, create_country_object, create_location_object,
    create_job_object, create_budget_object, award_project_bid,
    create_milestone_payment, release_milestone_payment,create_currency_object,
    get_bids,
)
from freelancersdk.exceptions import (
    ProjectNotCreatedException, BidsNotFoundException,
    BidNotAwardedException, MilestoneNotCreatedException,
    MilestoneNotReleasedException,
)
app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)
base_url = app.config['BASE_URL']
base_accounts_url = app.config['BASE_ACCOUNTS_URL']
client_id = app.config['CLIENT_ID']
client_secret = app.config['CLIENT_SECRET']
h = {"Freelancer-OAuth-V1": ''}
# A decorator that ensures a user is authenticated.
# The @authenticated tag should be used on any endpoints you
# want to protect by OAuth.
def authenticated(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        global h
        if not h["Freelancer-OAuth-V1"]:
            if 'Authorization' in session:
                h["Freelancer-OAuth-V1"] = session['Authorization']
        if db.session.query(User).filter(User.access_token == h["Freelancer-OAuth-V1"]).count() == 0:
            return auth()
        return f(*args, **kwargs)
    return decorated
# Authorise a user
@app.route('/auth')
def auth():
    oauth_uri = base_accounts_url + '/oauth/authorise'
    redirect_uri = 'http://127.0.0.1:5000/auth_redirect'
    prompt = 'select_account consent'
    advanced_scopes = '1 2 3 4 5 6'
    return redirect(
        '{0}?response_type=code&client_id={1}&redirect_uri={2}&scope=basic&prompt={3}&advanced_scopes={4}'.format(
            oauth_uri, client_id, redirect_uri, prompt, advanced_scopes
        )
    )
# This is the endpoint that catches the returned data from your Freelancer App.
@app.route('/auth_redirect')
def handle_redirect():
    authorisation_code = request.args['code']
    payload = {
        'grant_type': 'authorization_code',
        'code': authorisation_code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': 'http://127.0.0.1:5000/auth_redirect', 
    }
    response = requests.post(base_accounts_url + '/oauth/token', data=payload).json()
    h = {"Freelancer-OAuth-V1": response["access_token"]}
    url = base_url + "/api/users/0.1/self/"
    details = requests.get(url, headers=h).json()
    user = User(details['result']['username'], details["result"]['email'], response['access_token'], response['refresh_token'])	
    db.session.add(user)
    db.session.commit()
    session['Authorization'] = response['access_token']
    return render_template("user.html", user=user)
# Unauthenticate the user
@app.route('/logout')
def logout():
    session.pop('Authorization', None)
    return render_template("home.html")
# A sample route protected by authentication
@app.route('/behindauth')
@authenticated
def behindauth():
    return "You've revealed all the secrets! Your token is: " + h["Freelancer-OAuth-V1"]
# Create a project with the logged in user's credentials.
@app.route('/create_project', methods=["GET", "POST"])
@authenticated
def post_project():
    if request.method == "GET":
        return render_template("create_project.html")
    data = {
        'title': "Need someone to buy and bring me a beer ASAP.",
        'description': json.loads(request.data)['description'],
        'budget': create_budget_object(
            minimum=10,
            maximum=25,
        ),
        'currency': create_currency_object(id=3),
        'jobs': [create_job_object(id=632)],
        'location': create_location_object(
            country=create_country_object('Australia'),
            city='Sydney',
            latitude=-33.8744101,
            longitude=151.2028132,
            full_address="Sydney, NSW, Australia",
        )
    }
    result = None
        
    try:
        
        # TODO: Make this an app level attribute instead    
        s = Session(oauth_token=h["Freelancer-OAuth-V1"], url=base_url)
        result = create_local_project(s, **data)
    except ProjectNotCreatedException as e:
        print(('Error message: %s' % e.message))
        print(('Error code: %s' % e.error_code))
        return jsonify(result)
    else:
        result = {'result': {'id': result.id, 'seo_url': result.seo_url }}
        return jsonify(result)
@app.route('/')
@authenticated
def index():
    return render_template("button.html")
@app.route('/project/<int:project_id>/bids')
@authenticated
def getbids(project_id):
    get_bids_data = {
        'project_ids': [
            project_id,
        ],
        'limit': 10,
        'offset': 0,
    }
    try:
        # TODO: Make this an app level attribute instead
        s = Session(oauth_token=h["Freelancer-OAuth-V1"], url=base_url)
        data = get_bids(s, **get_bids_data)
    except BidsNotFoundException as e:
        print('Error message: {}'.format(e.message))
        print('Server response: {}'.format(e.error_code))
        return jsonify(data)
    else:
        result = {'result': data}
        return jsonify(result)
@app.route('/award/<int:bid_id>', methods=['PUT'])
@authenticated
def award_bid(bid_id):
    bid_data = {
        'bid_id': bid_id,
    }
    data = None
    try:
        # TODO: Make this an app level attribute instead
        s = Session(oauth_token=h["Freelancer-OAuth-V1"], url=base_url)
        data = award_project_bid(s, **bid_data)
    except BidNotAwardedException as e:
        print('Error message: {}'.format(e.message))
        print('Server response: {}'.format(e.error_code))
        return jsonify(data)
    else:
        return jsonify(data)
# Create a milestone
@app.route('/create_milestone', methods=["POST"])
@authenticated
def create_milestone():
    # get bid details
    bid_id = json.loads(request.data)['bid_id']
    get_bid_data = {
        'bid_ids': [
            bid_id,
        ],
    }
    try:
        # TODO: Make this an app level attribute instead
        s = Session(oauth_token=h["Freelancer-OAuth-V1"], url=base_url)
        response = get_bids(s, **get_bid_data)
    except BidsNotFoundException as e:
        print('Error message: {}'.format(e.message))
        print('Server response: {}'.format(e.error_code))
        return jsonify(response)
    # create the milestone
    response = response['bids'][0]
    milestone_data = {
        "bidder_id": response["bidder_id"],
        "amount": response["amount"],
        "project_id": response["project_id"],
        "reason": MilestoneReason.PARTIAL_PAYMENT.value,
        "description": "Full payment upon delivery."
    }
    data = None
    try:
        s = Session(oauth_token=h["Freelancer-OAuth-V1"], url=base_url)
        data = create_milestone_payment(s, **milestone_data)
    except MilestoneNotCreatedException as e:
        print(('Error message: %s' % e.message))
        print(('Server response: %s' % e.error_code))
        return jsonify(data)
    else:
        result = {'result': {'amount': data.amount, 'transaction_id': data.transaction_id}}
        return jsonify(result)

@app.route('/pay/<int:transaction_id>', methods=["PUT"])
@authenticated
def pay(transaction_id):
    milestone_data = {
        'milestone_id': transaction_id,
        'amount': json.loads(request.data)["amount"],
    }
    data = None
    try:
        s = Session(oauth_token=h["Freelancer-OAuth-V1"], url=base_url)
        data = release_milestone_payment(s, **milestone_data)
    except MilestoneNotReleasedException as e:
        print(('Error message: %s' % e.message))
        print(('Server response: %s' % e.error_code))
        return jsonify(data)
    else:
        return jsonify(data)
