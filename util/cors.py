def pre_cors(req, resp, params):
  resp.set_header('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
  resp.set_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')

def post_cors(req, resp):
  resp.set_header('Access-Control-Allow-Origin', '*')
