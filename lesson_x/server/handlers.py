import json
from protocol import validate_request, make_response
from resolvers import resolve
from middlewares import compression_middleware, encryption_middleware


@compression_middleware
@encryption_middleware
def handle_default_request(raw_request, logger):
    request = json.loads(raw_request.decode())
    print(f'request: {request}')

    if validate_request(request):
        action_name = request.get('action')
        controller = resolve(action_name)
        # -----------------------------------------------
        if controller:

            try:
                logger.debug(f'Controller {controller} resolved with request: {request}')
                # print(f'Controller {controller} resolved with request: {request}')
                # response = make_response(request, 200, request.get('data'))
                response = controller(request)

            except Exception as err:
                logger.critical(f'Controller {controller} error: {err}')
                # print(f'Controller {controller} error: {err}')
                response = make_response(request, 500, 'Internal Server  Error!')
        # ------------------------------------------------
        else:
            logger.error(f'Controller {controller} not found!')
            # print(f'Controller {controller} not found!')
            response = make_response(request, 404, f'Action with name {action_name} is not supported!')

    else:
        logger.error(f'Wrong request!')
        # print(f'Wrong request!')
        response = make_response(request, 400, 'Wrong request format!')

    return json.dumps(response).encode()
