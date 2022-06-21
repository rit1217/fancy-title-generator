from multiprocessing.pool import ApplyResult
from .api import app

# print([str(p) for p in ApplyResult.url_map.iter_rules()])
app.run(host='0.0.0.0', port=3100)