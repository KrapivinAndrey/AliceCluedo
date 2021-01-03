class AliceResponse:

    def __init__(self, request):

        self._response_dict = {
            'version': request['version'],
            'session': request['session'],
            'response': {
                'end_session': False
            }
        }

    def get(self, path):
        result = self._response_dict
        for a in path.split('.'):
            result = result[a]
        return result
