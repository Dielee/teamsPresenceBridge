# Teams Presence Bridge
Python tool to fetch MS Teams status from GraphAPI.

## 1. Setup Azure app

1.1  Login with your company MS account and Register an new app here: [Azure Portal](https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade "Azure Portal")

1.2  Give your app an name, set Supported Account Types to: `Only accounts in this organizational directory` and the redirect URL to: `https://login.microsoftonline.com/common/oauth2/nativeclient`

1.3  Copy and store the applicationId and the tennantId from the dashboard, you need those later!

1.4 In the left sidebar, go to Certificates & secrets. Than, create an new secret clientkey.
Copy and store the clientkey, not the Id!

1.5 In the left sidebar, go to "API-Rights", than "Add-Rights".
Choose "Microsoft Graph" and "Delegated rights".
Search and tick "offline_acces" and "Presence_read".

##  2. Setup teamsPresenceBridge
#### a. Local install

2.1 Clone repository `git clone https://github.com/Dielee/teamsPresenceBridge.git`

2.2 Fill src/config.yaml with your azure data from step one.

2.3 Run the application from src directory with python on windows or linux with:
`python3 .\server.py`

2.4 Authenticate your application with graph api. Open your browser an go to `http://ipApplicationRunsAt:5557/getRequestURL`. If everything has been configured correctly, you will now be asked whether the app should be authorized. Select "Yes" and then copy the forwarded URL in the browser. Next, go to `http://ipApplicationRunsAt:5557/getToken?url=yourRequestURL` and paste the copied request URL from /getRequestURL.  Now, you should see an `Authentication successful, token stored!`. If not, try again from step one and check all keys and tokens.

2.5 If everything worked, you can fetch your presence state with `http://ipApplicationRunsAt:5557/getPresence` 

#### b. Docker install

2.1 Pull container `docker pull dielee/teamspresencebridge`

2.2 Start container `docker run -d -p 5557:5557 -e azureApplicationId="applicationId" -e azureClientKey="<clientKey>" -e azureTenantId="<tenantId>" teamspresencebridge:latest`

2.3 Authenticate your application with graph api. Open your browser an go to `http://ipApplicationRunsAt:5557/getRequestURL`. If everything has been configured correctly, you will now be asked whether the app should be authorized. Select "Yes" and then copy the forwarded URL in the browser. Next, go to `http://ipApplicationRunsAt:5557/getToken?url=yourRequestURL` and paste the copied request URL from /getRequestURL.  Now, you should see an `Authentication successful, token stored!`. If not, try again from step one and check all keys and tokens.

2.4 If everything worked, you can fetch your presence state with `http://ipApplicationRunsAt:5557/getPresence` 

