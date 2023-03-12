from bottle import route, run, template
from datetime import datetime

@route("/")
def index():
    dt = datetime.now()
    time = "{:%Y-%m-%d %H:%M:%S}".format(dt)
    return template("<b>Pi thinks the time/date is: {{t}}</b>", t=time)

run(host="0.0.0.0", port=8080, debug=True)
