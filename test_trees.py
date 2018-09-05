import http.client
import inspect


def request(method, path, body='', headers={}):
    conn = http.client.HTTPConnection('127.0.0.1', 8000)
    conn.request(method, path, body, headers)
    response = conn.getresponse()
    conn.close()

    return response.status, response.reason, response.read()


def assert_comparison(exp, resp):
    comparison = [(exp == resp) for exp, resp in zip(exp, resp)]

    if len(set(comparison)) == 1 and list(set(comparison))[0] is True:
        return True

    return False


def run_tests(obj):
    print('Running tests...')
    failed = []
    for name in dir(obj):
        method = getattr(obj, name)
        if name.startswith('test_') and inspect.ismethod(method):
            if method():
                print('.', end='')
            else:
                failed.append(name)
                print('F', end='')
    print()

    if len(failed) > 0:
        print('Following tests have failed: ' + ', '.join(failed))


class TestApi():
    def test_get_method_request_returns_405(self):
        expected = (
            405,
            'Method Not Allowed',
            b'405 Method not allowed'
        )

        response = request(
            'GET',
            '/',
        )

        return assert_comparison(expected, response)

    def test_put_method_request_returns_405(self):
        expected = (
            405,
            'Method Not Allowed',
            b'405 Method not allowed'
        )

        response = request(
            'PUT',
            '/',
        )

        return assert_comparison(expected, response)

    def test_patch_method_request_returns_405(self):
        expected = (
            405,
            'Method Not Allowed',
            b'405 Method not allowed'
        )

        response = request(
            'PATCH',
            '/',
        )

        return assert_comparison(expected, response)

    def test_delete_method_request_returns_405(self):
        expected = (
            405,
            'Method Not Allowed',
            b'405 Method not allowed'
        )

        response = request(
            'DELETE',
            '/',
        )

        return assert_comparison(expected, response)

    def test_post_request_returns_422_when_body_is_invalid_json(self):
        expected = (
            422,
            'Unprocessable Entity',
            b'422 Unprocessable Entity'
        )

        response = request(
            'POST',
            '/',
            '"favoriteTree": "baobab"}',
            {'Content-type': 'application/json'}
        )

        return assert_comparison(expected, response)

    def test_post_request_returns_422_when_empty_payload(self):
        expected = (
            422,
            'Unprocessable Entity',
            b'422 Unprocessable Entity'
        )

        response = request(
            'POST',
            '/',
            '',
            {'Content-type': 'application/json'}
        )

        return assert_comparison(expected, response)

    def test_post_request_returns_415_when_content_type_is_not_json(self):
        expected = (
            415,
            'Unsupported Media Type',
            b'415 Unsupported Media Type'
        )

        response = request(
            'POST',
            '/',
            '{"favoriteTree": "baobab"}',
            {'Content-type': 'application/xml'}
        )

        return assert_comparison(expected, response)

    def test_post_request_returns_404_if_URL_is_not_index(self):
        expected = (
            404,
            'Not Found',
            b'404 Not Found'
        )

        response = request(
            'POST',
            '/api',
            '{"favoriteTree": "baobab"}',
            {'Content-type': 'application/json'}
        )

        return assert_comparison(expected, response)

    def test_post_request_asks_for_favourite_tree_when_not_in_payload(self):
        expected = (
            200,
            'OK',
            b'Please tell me your favorite tree.'
        )

        response = request(
            'POST',
            '/',
            '{"tree": "baobab"}',
            {'Content-type': 'application/json'}
        )

        return assert_comparison(expected, response)

    def test_post_request_asks_for_favourite_tree_when_favourite_is_number(self):
        expected = (
            200,
            'OK',
            b'Please tell me your favorite tree.'
        )

        response = request(
            'POST',
            '/',
            '{"favoriteTree": 2}',
            {'Content-type': 'application/json'}
        )

        return assert_comparison(expected, response)

    def test_post_request_asks_for_favourite_tree_when_empty_payload(self):
        expected = (
            200,
            'OK',
            b'Please tell me your favorite tree.'
        )

        response = request(
            'POST',
            '/',
            '{}',
            {'Content-type': 'application/json'}
        )

        return assert_comparison(expected, response)

    def test_post_request_returns_favourite_tree(self):
        expected = (
            200,
            'OK',
            b"It's nice to know that your favorite tree is a baobab!"
        )

        response = request(
            'POST',
            '/',
            '{"favoriteTree": "baobab"}',
            {'Content-type': 'application/json'}
        )

        return assert_comparison(expected, response)

run_tests(TestApi())
