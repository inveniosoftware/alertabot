# Deploy on OpenShift

Helm charts are provided in this repository to easily deploy the application in a couple of steps

1. Create a project on OpenShift
2. Login to OpenShift and switch to the created project
```
oc project alertabot
```
3. Change the `alertabot.hostname` in the `helm/values.yaml` with your desired base URL (e.g. `alertabot.web.cern.ch`)

4. Create secrets with the configuration values

| Value          | Description                                                                                                                                        |
|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| DISCORD_TARGET | The webhook URL of the Discord channel where alertabot will post notification.                                                                     |
| WEBHOOK_TOKEN  | A random (long) string. `<alertabot.hostname>/webhook/<STRING>` will then be the Endpoint URL exposed by this application (configure Harbor to post there).  |
| SENTRY_DSN     | DNS from the Sentry (Python) Project you created to monitor the application.                                                                       |

E.g.:
```
oc create secret generic \
--from-literal="DISCORD_TARGET=<VALUE>" \
--from-literal="WEBHOOK_TOKEN=<VALUE>" \
--from-literal="SENTRY_DSN=h<VALUE>" \
alertabot-secrets
```

5. Install the helm charts
```
helm install alertabot helm
```

Check `<alertabot.hostname>/health` to see if the endpoints are up.
