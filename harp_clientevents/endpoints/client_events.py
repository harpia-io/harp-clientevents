from microservice_template_core.tools.flask_restplus import api
from flask_restplus import Resource
from flask import request
from microservice_template_core.tools.logger import get_logger
import harp_clientevents.settings as settings


logger = get_logger()
ns = api.namespace('api/v1/clientevents', description='Harp client events endpoints')


@ns.route('/logs')
class ClientEvents(Resource):

    @staticmethod
    def post():
        """
        Send client logs to Loki
        Use this method to send client logs to Loki
        * Send a JSON object
        ```
        {
            "severity": "error", (possible options - info|warning|error)
            "message": "Some message from client",
            "event_name": "Some name of the event",
            "tags": {
                "client_version": 1,
                "browser": "chrome",
                "some_custom_tag": "tag"
            }
        }
        ```
        """
        data = request.get_json()

        try:
            if 'severity' not in data:
                return 'Severity should be specified', 404
            if 'message' not in data:
                return 'Message should be specified', 404
            if 'event_name' not in data:
                return 'Event_name should be specified', 404
            if data['severity'] not in ['info', 'warning', 'error']:
                return 'Severity is not correct. Available options - info|warning|error', 404

            event_tags = {
                'namespace': settings.SERVICE_NAMESPACE,
                'event_name': data['event_name']
            }

            if 'tags' in data:
                if data['tags']:
                    event_tags.update(data['tags'])

            if data['severity'] == 'info':
                logger.info(
                    msg=str(data['message']),
                    extra={'tags': event_tags}
                )

            if data['severity'] == 'warning':
                logger.warning(
                    msg=str(data['message']),
                    extra={'tags': event_tags}
                )

            if data['severity'] == 'error':
                logger.error(
                    msg=str(data['message']),
                    extra={'tags': event_tags}
                )
        except Exception as err:
            logger.error(msg=f"Can`t push client logs to Loki\nError - {err}\nData: {data}")
            return 'Can`t push client logs to Loki. Error - {err}. Mode details in logs', 400

        return 'Logs have been sent to Loki', 200
