import flask, json, sys, os

app = flask.Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['DEBUG'] = True

root_url = 'https://localhost:5000/'

@app.route('/', defaults={'path': ''}, methods=['OPTIONS'])
@app.route('/<path:path>', methods=['OPTIONS'])
def options(path):
    resp = flask.Response("")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    resp.headers["Access-Control-Allow-Headers"] = "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"
    return resp

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def route(path):
    path = path.split('/')
    event = {
        'httpMethod': flask.request.method,
        'body': flask.request.get_data().decode(),
        'headers': {
            'Host': flask.request.host,
            'X-Forwarded-Proto': root_url.split('://')[0],
        },
        'requestContext': {
            'stage': path[0],
            'resourcePath': '/' + '/'.join(path[1:]),
        }
    }
    res = lambda_handler(event, None)
    if int(res['statusCode'] / 100) == 3:
        return flask.redirect(res['headers'].get('Location', ''), res['statusCode'])

    resp = flask.Response(res['body'])
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

def local_test():
    if 'https://' in root_url:
        ctx = ('certs/localhost.crt', 'certs/localhost.key')
    else:
        ctx = None
    app.run(ssl_context=ctx)

if __name__ == '__main__':
    assert(len(sys.argv) > 1)
    sys.path.append(os.path.dirname(sys.argv[1]))
    from lambda_package import lambda_handler
    local_test()

