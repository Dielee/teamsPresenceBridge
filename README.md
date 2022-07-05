# Teams Presence Bridge

Python tool to fetch MS Teams status from GraphAPI and present it as RestApi.

## 1. Setup Azure app

1.1 Login with your company MS account and Register a new app here: [Azure Portal](https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade)

1.2 Give your app a name, set supported account types to: `Only accounts in this organizational directory` and the redirect URL to: `https://login.microsoftonline.com/common/oauth2/nativeclient`

1.3 Copy and store the applicationId and the tennantId from the dashboard, you need those later!

1.4 In the left sidebar, go to Certificates & secrets. Then, create a new secret clientkey. Copy and store the clientkey, not the Id!

1.5 In the left sidebar, go to "API-Rights", than "Add-Rights". Choose "Microsoft Graph" and "Delegated rights". Search and tick "offline_access" and "Presence.read".

##  2. Setup teamsPresenceBridge
There are several ways to install this. 
You can use it locally, as [Home assistant Add-On](https://www.home-assistant.io/addons/) or as docker container. 
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

#### b. Home assistant install
[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fyouseeus%2FteamsPresenceBridge)

Use the button above or add the URL of this repository to add it manually.
Or follow the steps at the [HomeAssistant docs](https://developers.home-assistant.io/docs/add-ons/tutorial#step-2-installing-and-testing-your-add-on)
#### c. Docker install

2.1 Pull container `docker pull dielee/teamspresencebridge:latest`

2.2 Start container `docker run -d -p 5557:5557 -e azureApplicationId="applicationId" -e azureClientKey="<clientKey>" -e azureTenantId="<tenantId>" teamspresencebridge:latest`

2.3 Authenticate your application with graph api. Open your browser and go to `http://dockerIp:5557/getRequestURL`.
If everything has been configured correctly, you will now be asked whether the app should be authorized.
Select "Yes" and then copy the forwarded URL in the browser.
Next, go to `http://dockerIp:5557/getToken?url=yourRequestURL` and paste the copied request URL from /getRequestURL.  
Now, you should see an `Authentication successful, token stored!`. If not, try again from step one and check all keys and tokens.

2.4 If everything worked, you can fetch your presence state with `http://dockerIp:5557/getPresence`


## 3. Setup Teams host state (optional)
If you want to monitor not only the teams status, but also the status of the pc running teams, you can report every four minutes to the teamspresencebridge that the pc is still online. You can do this using the examples in the setTeamsHostOnline folder.

## 4. Troubleshooting
###  AADSTS700025: Client is public so neither 'client_assertion' nor 'client_secret' should be presented.
if you get an `Authentication error` and in the server logs an `AADSTS700025: Client is public so neither 'client_assertion' nor 'client_secret' should be presented.`
check in the [Azure Portal](https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade) -> Authentication
the platform shoud be web and the toggle `Allow public client flows` is on `no`


[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg