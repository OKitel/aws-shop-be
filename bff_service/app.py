from flask import Flask, request, Response, stream_with_context
import requests
from os import getenv
from dotenv import load_dotenv
from werkzeug.exceptions import BadGateway, InternalServerError
import logging

load_dotenv()

class Config:
    PORT = 3000
    DEBUG = True

app = Flask(__name__)
app.config.from_object(Config)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_service_url(service):
    """Retrieve the service URL from environment variables."""
    service_url = getenv(service)
    if not service_url:
        logger.error(f"Service URL for {service} not found.")
        raise BadGateway(f"Cannot process request")
    return service_url

def create_proxy_request(full_url):
    """Create and send the proxy request."""
    return requests.request(
        method=request.method,
        url=full_url,
        headers={key: value for key, value in request.headers if key.lower() != 'host'},
        data=request.get_data(),
        allow_redirects=False,
        stream=True
    )

@app.route('/<service>',  defaults={'subpath': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/<service>/', defaults={'subpath': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/<service>/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def proxy(service, subpath):
    """Proxy the request to the appropriate service."""
    try:
        service_url = get_service_url(service)
        full_url = f"{service_url}/{subpath}?{request.query_string.decode()}"
        
        response = create_proxy_request(full_url)

        return Response(
            stream_with_context(response.iter_content(chunk_size=4096)),
            status=response.status_code,
            headers={key: value for key, value in response.headers.items() if key.lower() != 'content-encoding'},
            content_type=response.headers.get('Content-Type', 'application/json')
        )
    except Exception as e:
        logger.exception(f"Failed to proxy request: {e}")
        raise

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'])
