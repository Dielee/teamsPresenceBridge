from O365 import Account, FileSystemTokenBackend
from flask import Flask, redirect, request
import json, os, datetime
from util import loadConfFromFile, loadConfFromVar

runMode = os.environ.get('RUN_IN_DOCKER', False)
if runMode:
    print("Running in docker mode, load conf from env...")
    cfg = loadConfFromVar()
else:
    print("Running in other mode, load conf from file...")
    cfg = loadConfFromFile()

credentials = (cfg['azureApplicationId'], cfg['azureClientKey'])
tenantId = cfg['azureTenantId']

app = Flask(__name__)
callback = 'https://login.microsoftonline.com/common/oauth2/nativeclient'
authAccount  = None
lastOnline = None

@app.before_first_request
def first():
    if os.path.isfile('o365_token.txt'):
        global authAccount
        token_backend = FileSystemTokenBackend(token_filename='o365_token.txt')
        authAccount = Account(credentials, tenant_id=tenantId, token_backend=token_backend)

@app.route('/getRequestURL')
def auth_step_one():
    
    account = Account(credentials, tenant_id=tenantId)
    url = account.con.get_authorization_url(requested_scopes=["Presence.Read", "offline_access"], redirect_uri=callback)
    
    return redirect(url[0])

@app.route('/getToken')
def auth_step_two_callback():
    global authAccount
    account = Account(credentials, tenant_id=tenantId)

    redirectURL = request.args.get('url')
    result = account.con.request_token(redirectURL, redirect_uri=callback)

    if result:
        authAccount = account
        return "Authentication successful, token stored!"
    else:
        return "Authentication failed, try again"

@app.route('/getPresence')
def getPresence():
    if(authAccount):
        if(authAccount.is_authenticated):
            teamsHostState = getTeamsHostState()

            lastOnlineStr = None
            if lastOnline:
                lastOnlineStr = lastOnline.strftime("%c")

            if (teamsHostState == "online" or teamsHostState == "undefined"):
                myPresence = authAccount.teams().get_my_presence().activity
                retJson = {'state': myPresence, 'attributes': {'teamsHostStatus': teamsHostState, 'lastOnlineReport': lastOnlineStr}}

                return json.dumps(retJson)
            else:
                retJson = {'state': 'offline', 'attributes': {'teamsHostStatus': teamsHostState, 'lastOnlineReport': lastOnlineStr}}

                return json.dumps(retJson)
        else:
            return "Unauthorized! Run /getRequestURL and than /getToken?url= "
    else:
        return "Unauthorized! Run /getRequestURL and than /getToken?url= "

@app.route('/setOnline')
def setOnline():
    global lastOnline
    lastOnline = datetime.datetime.now()

    return "Online status set!"

def getTeamsHostState():
    if(not lastOnline):
        return "undefined"

    minutesDiff = (datetime.datetime.now() - lastOnline).total_seconds() / 60

    if (minutesDiff < 5):
        return "online"
    else:
        return "offline"