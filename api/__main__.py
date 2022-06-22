from multiprocessing.pool import ApplyResult
from .api import app

# print([str(p) for p in ApplyResult.url_map.iter_rules()])
app.run(use_reloader=True, host='0.0.0.0', port=3000)