# Teams Presence Bridge
Python tool to fetch MS Teams status from GraphAPI.

## 1. Setup Azure app

1.1 Login with your company MS account and Register a new app here: [Azure Portal](https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade)

1.2 Give your app a name, set supported account types to: `Only accounts in this organizational directory` and the redirect URL to: `https://login.microsoftonline.com/common/oauth2/nativeclient`

1.3 Copy and store the applicationId and the tennantId from the dashboard, you need those later!

1.4 In the left sidebar, go to Certificates & secrets. Then, create a new secret clientkey. Copy and store the clientkey, not the Id!

1.5 In the left sidebar, go to "API-Rights", than "Add-Rights". Choose "Microsoft Graph" and "Delegated rights". Search and tick "offline_access" and "Presence.read".

##  2. Setup teamsPresenceBridge
#### a. Local install

2.1 Clone repository `git clone https://github.com/Dielee/teamsPresenceBridge.git`

2.2 Install requirements with `pip3 install -r requirements.txt`

2.3 Fill src/config.yaml with your azure data from step one.

2.4 Run the application from src directory with python on windows or linux with:
`python3 .\server.py`

2.5 Authenticate your application with graph api. Open your browser and go to `http://ipApplicationRunsAt:5557/getRequestURL`. 
If everything has been configured correctly, you will now be asked whether the app should be authorized. 
Select "Yes" and then copy the forwarded URL in the browser. 
Next, go to `http://ipApplicationRunsAt:5557/getToken?url=yourRequestURL` and paste the copied request URL from /getRequestURL.  
Now, you should see an `Authentication successful, token stored!`. If not, try again from step one and check all keys and tokens.

2.6 If everything worked, you can fetch your presence state with `http://ipApplicationRunsAt:5557/getPresence` 

#### b. Docker install

2.1 Pull container `docker pull dielee/teamspresencebridge:latest`

2.2 Start container `docker run -d -p 5557:5557 -e azureApplicationId="applicationId" -e azureClientKey="<clientKey>" -e azureTenantId="<tenantId>" teamspresencebridge:latest`

2.3 Authenticate your application with graph api. Open your browser and go to `http://dockerIp:5557/getRequestURL`. 
If everything has been configured correctly, you will now be asked whether the app should be authorized. 
Select "Yes" and then copy the forwarded URL in the browser. 
Next, go to `http://dockerIp:5557/getToken?url=yourRequestURL` and paste the copied request URL from /getRequestURL.  
Now, you should see an `Authentication successful, token stored!`. If not, try again from step one and check all keys and tokens.

2.4 If everything worked, you can fetch your presence state with `http://dockerIp:5557/getPresence` 

## 3. Setup HomeAssistant

3.1 Setup sensor:
``` yaml
  - platform: rest
    name: TeamsPresence
    method: GET
    resource: 'http://192.168.50.2:5557/getPresence'
    value_template: '{{ value_json["state"] }}'
    json_attributes_path: 'attributes'
    json_attributes:
      - 'teamsHostStatus'
      - 'lastOnlineReport'
    scan_interval: 2
```
3.2 Setup automation:
``` yaml
alias: SetTeamsLight
description: ''
trigger:
  - platform: state
    entity_id: sensor.teamspresence
condition:
  - condition: state
    entity_id: sensor.teamspresence
    state: online
    attribute: teamsHostStatus
action:
  - service: light.turn_on
    entity_id: light.presencelight
    data_template:
      rgb_color: |
        {% if states('sensor.teamspresence') == 'Available' %}
          [0,255,63]
        {% elif states('sensor.teamspresence') == 'Busy' or
          states('sensor.teamspresence') == 'DoNotDisturb' or
          states('sensor.teamspresence') == 'InACall' or
          states('sensor.teamspresence') == 'InAMeeting' or
          states('sensor.teamspresence') == 'Presenting' or
          states('sensor.teamspresence') == 'InAConferenceCall'
        %}
          [255,0,0]
        {% elif states('sensor.teamspresence') == 'BeRightBack' or
                states('sensor.teamspresence') == 'Away' or
                states('sensor.teamspresence') == 'Inactive' %}
          [255,190,0]
        {% else %} [145, 226, 255] {% endif %}
      brightness: 1
mode: single

```

## 4. Setup Teams host state (optional)
If you want to monitor not only the teams status, but also the status of the pc running teams, you can report every four minutes to the teamspresencebridge that the pc is still online. You can do this using the examples in the setTeamsHostOnline folder.
