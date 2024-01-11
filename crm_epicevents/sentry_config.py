import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://a7d4386abec0cdbcf8f8826cb04c20aa@o4506546482511872.ingest.sentry.io/4506546484215808",
    integrations=[DjangoIntegration()],
    debug=True,
)
