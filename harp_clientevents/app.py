from microservice_template_core import Core
from microservice_template_core.settings import ServiceConfig, FlaskConfig, DbConfig
from harp_clientevents.endpoints.client_events import ns as client_events
from harp_clientevents.endpoints.health import ns as health


def main():
    ServiceConfig.configuration['namespaces'] = [client_events, health]
    FlaskConfig.FLASK_DEBUG = False
    DbConfig.USE_DB = False
    app = Core()
    app.run()


if __name__ == '__main__':
    main()

