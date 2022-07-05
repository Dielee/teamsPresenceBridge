
## 1. Setup Azure app

1.1 Login with your company MS account and Register a new app here: [Azure Portal](https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade)

1.2 Give your app a name, set supported account types to: `Only accounts in this organizational directory` and the redirect URL to: `https://login.microsoftonline.com/common/oauth2/nativeclient`

1.3 Copy and store the applicationId and the tennantId from the dashboard, you need those later!

1.4 In the left sidebar, go to Certificates & secrets. Then, create a new secret clientkey. Copy and store the clientkey, not the Id!

1.5 In the left sidebar, go to "API-Rights", than "Add-Rights". Choose "Microsoft Graph" and "Delegated rights". Search and tick "offline_access" and "Presence.read".

## 2. HomeAssistant

Setup sensor:
``` yaml
  - platform: rest
    name: TeamsPresence
    method: GET
    resource: "http://localhost:5557/getPresence"
    value_template: '{{ value_json["state"] }}'
    json_attributes_path: "attributes"
    json_attributes:
      - "teamsHostStatus"
      - "lastOnlineReport"
    scan_interval: 2
```
Setup automation:
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

## 4. Troubleshooting
###  AADSTS700025: Client is public so neither 'client_assertion' nor 'client_secret' should be presented.
If you get an `Authentication error` and in the server logs an `AADSTS700025: Client is public so neither 'client_assertion' nor 'client_secret' should be presented.`
check in the [Azure Portal](https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade) -> Authentication.
The platform should be `web` and the toggle `Allow public client flows` on `no`
