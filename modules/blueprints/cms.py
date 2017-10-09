import json, time
from ast import literal_eval

from flask import Blueprint, render_template, abort, current_app, session, request, Markup, jsonify

from modules.db import *
from modules.decorators import *
from modules import query
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.http import HttpError


cms_views = Blueprint('cms_views', __name__, template_folder='templates')       #blueprint definition


def get_service(api_name, api_version, scopes, key_file_location):
    """Get a service that communicates to a Google API.

    Args:
      api_name: The name of the api to connect to.
      api_version: The api version to connect to.
      scope: A list auth scopes to authorize for the application.
      key_file_location: The path to a valid service account JSON key file.

    Returns:
      A service that is connected to the specified API.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        current_app.config['GOOGLE_API_JSON'], scopes=scopes)
    # Build the service object.
    service = build(api_name, api_version, credentials=credentials)

    return service


def get_profile_id(account):
    # Use the Analytics service object to get the profile id.
    service = get_analytics_service()
    properties = service.management().webproperties().list(
            accountId=account).execute()
    if properties.get('items'):
        property = properties.get('items')[0].get('id')
        profiles = service.management().profiles().list(
            accountId=account,
            webPropertyId=property).execute()

        if profiles.get('items'):
            return profiles.get('items')[0].get('id')

    return None


def get_results(service, profile_id, metric, start_date, end_date):
    # Use the Analytics Service Object to query the Core Reporting API
    return service.data().ga().get(
          ids='ga:' + profile_id,
          start_date=start_date,
          end_date=end_date,
          metrics=metric).execute()


def get_analytics_service():
    key_file_location = current_app.config['GOOGLE_API_JSON']
    scopes = ['https://www.googleapis.com/auth/analytics.readonly']
    service = get_service('analytics', 'v3', scopes, key_file_location)
    return service


def get_accounts():
    service = get_analytics_service()
    accounts = service.management().accounts().list().execute()
    return [(x['name'].encode('utf-8'), int(x['id'])) for x in accounts.get('items')]


def get_total_metric(account, metric, start_date, end_date):
    # Use the Analytics Service to get total metric info
    key_file_location = current_app.config['GOOGLE_API_JSON']
    scopes = ['https://www.googleapis.com/auth/analytics.readonly']

    # Authenticate and construct service.
    service = get_service('analytics', 'v3', scopes, key_file_location)
    profile = get_profile_id(account)
    results = get_results(service, profile, metric, start_date, end_date)
    try:
        summary = results.get('rows')[0][0]
    except TypeError:
        summary = 0
    return summary


def get_metadata_rows():
    # Get all available metrics for current Analitics Account
    service = build('analytics', 'v3', developerKey=current_app.config['GOOGLE_API_KEY'])
    try:
        results = service.metadata().columns().list(reportType='ga').execute()
    except TypeError, error:
        # Handle errors in constructing a query.
        return ('There was an error in constructing your query : %s' % error)
    except HttpError, error:
        # Handle API errors.
        return ('Arg, there was an API error : %s : %s' %
             (error.resp.status, error._get_reason()))

    return results['items']


@cms_views.route('/view_posts')
@cms_views.route('/view_posts/')
@admin_required(current_app, session, 'login_routes.login_redirect')
@with_user_data(current_app, session)
def view_posts(user_data=None):
    ctl = current_app.config['ctl']
    data = {}
    data["ts"] = int(time.time())

    data["page_specific_js"] = ["/static/js/Requests.js", "/static/js/PostManager.js" ]
    data["post_action_bar"] = render_template("/post_actions.html")

    if user_data:
        data["user_data"] = user_data

    db_wrapper = database_wrapper()
    posts = query.getAllPosts(db_wrapper.content)

    if posts:
        data["posts"] = posts

    return render_template("/view_posts.html", data = data)



@cms_views.route('/edit/<int:post_id>')
@cms_views.route('/edit/<int:post_id>/')
@admin_required(current_app, session, 'login_routes.login_redirect')
@with_user_data(current_app, session)
def edit_post(post_id, user_data=None):
    ctl = current_app.config['ctl']
    data = {}
    data["ts"] = int(time.time())

    db_wrapper = database_wrapper()

    data["post_data"] = ctl.get_post_content(db_wrapper.content, post_id)

    data["page_specific_js"] = [ "/static/js/Requests.js", "/static/js/PostEditor.js" ]

    if user_data:
        data["user_data"] = user_data
    metadata = get_metadata_rows()
    accounts = get_accounts()

    return render_template("/post_editor.html", data = data, metadata=metadata, accounts=accounts)




@cms_views.route('/settings/')
@cms_views.route('/settings')
@admin_required(current_app, session, 'login_routes.login_redirect')
@with_user_data(current_app, session)
def settings(user_data=None):
    ctl = current_app.config['ctl']
    db_wrapper = database_wrapper()

    data = {}
    data["ts"] = int(time.time())

    data["database_settings"]  = db_wrapper.getDatabaseSettings(db_wrapper.config)
    data["redis_settings"]  = db_wrapper.getRedisSettings(db_wrapper.config)
    
    data["page_specific_js"] = [ "/static/js/Requests.js", "/static/js/Settings.js" ]

    if user_data:
        data["user_data"] = user_data

    return render_template("/settings.html", data = data)





@cms_views.route('/savePost/', methods = ['POST'])
@cms_views.route('/savePost', methods = ['POST'])
@admin_required(current_app, session, 'login_routes.login_redirect')
@with_user_data(current_app, session)
def save_post(user_data=None):
    ctl = current_app.config['ctl']

    postData = request.form['postData']
    postData = json.loads(postData)

    db_wrapper = database_wrapper()
    
    r = query.savePost(db_wrapper.content, postData)

    if r:
        db_wrapper.content.commit()

    return json.dumps(r)



@cms_views.route('/createPost/', methods = ['POST'])
@cms_views.route('/createPost', methods = ['POST'])
@admin_required(current_app, session, 'login_routes.login_redirect')
@with_user_data(current_app, session)
def create_post(user_data=None):
    ctl = current_app.config['ctl']

    postData = request.form['postData']
    postData = json.loads(postData)


    db_wrapper = database_wrapper() 
    
    post_id = query.createPost(db_wrapper.content, postData)

    if post_id:
        db_wrapper.content.commit()

    return json.dumps(post_id)




@cms_views.route('/deletePost/', methods = ['POST'])
@cms_views.route('/deletePost', methods = ['POST'])
@admin_required(current_app, session, 'login_routes.login_redirect')
@with_user_data(current_app, session)
def delete_post(user_data=None):
    ctl = current_app.config['ctl']

    postData = request.form['postData']
    postData = json.loads(postData)
    
    db_wrapper = database_wrapper()
    
    r = query.deletePost(db_wrapper.content, postData)

    if r:
        db_wrapper.content.commit()

    return json.dumps(r)


@cms_views.route('/bulkDeletePosts/', methods = ['POST'])
@cms_views.route('/bulkDeletePosts', methods = ['POST'])
@admin_required(current_app, session, 'login_routes.login_redirect')
@with_user_data(current_app, session)
def bulk_delete_posts(user_data=None):
    ctl = current_app.config['ctl']

    selectedPostIDs = request.form['selectedPostIDs']
    selectedPostIDs = json.loads(selectedPostIDs)

    db_wrapper = database_wrapper()
    
    r = query.bulkDeletePosts(db_wrapper.content, selectedPostIDs)

    if r:
        db_wrapper.content.commit()

    return json.dumps(r)





@cms_views.route('/saveRedisConfig/', methods = ['POST'])
@cms_views.route('/saveRedisConfig', methods = ['POST'])
@admin_required(current_app, session, 'login_routes.login_redirect')
@with_user_data(current_app, session)
def save_redis_config(user_data=None):
    ctl = current_app.config['ctl']
    db_wrapper = database_wrapper()

    redisConfig = request.form['redisConfig']
    redisConfig = json.loads(redisConfig)

    r = db_wrapper.saveRedisConfig(db_wrapper.config, redisConfig)

    if r:
        db_wrapper.config.commit()

    return json.dumps(r)




@cms_views.route('/saveDatabaseConfig/', methods = ['POST'])
@cms_views.route('/saveDatabaseConfig', methods = ['POST'])
@admin_required(current_app, session, 'login_routes.login_redirect')
@with_user_data(current_app, session)
def save_database_config(user_data=None):
    ctl = current_app.config['ctl']
    db_wrapper = database_wrapper()

    databaseConfig = request.form['databaseConfig']
    databaseConfig = json.loads(databaseConfig)

    r = db_wrapper.saveDatabaseConfig(db_wrapper.config, databaseConfig)

    if r:
        db_wrapper.config.commit()

    return json.dumps(r)


@cms_views.route('/_get_metric')
def _get_metric():
    """Get value of metric by user query.

    Query strings:
      metric: The name of the metric.
      expected: Expected metric value.
      start_date: Date of started collect metric.
      end_date: Date of ended collect metric.

    Returns:
        {
            'expected': 12.0,
            'result': 10.0
        }
    If errors:
        {
            'error': True,
            'result': Text of error,
        }
    """
    raw_account = request.args.get('account')
    account = int(literal_eval(raw_account)[1])
    print(account)
    metric = request.args.get('metric')
    expected = request.args.get('expected')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    error = ''

    if any(not v for v in list(request.args.values())):
       return jsonify({'error': True, 'result': "You need to fill all fields"})
    try:
        result = get_total_metric(account, metric, start_date, end_date)
    except (HttpError, TypeError) as e:
        print(e)
        error = "Unknown metric: {}".format(metric)

    if error:
        return jsonify({'error': True, 'result': error})

    return jsonify({'expected': float(expected), 'result': float(result)})
