from flask import Flask, Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import random, time
import psutil  # dodaj ovo

app = Flask(__name__)

# Custom metrics
REQUEST_COUNT = Counter('app_request_count', 'Total HTTP Requests')
LATENCY = Histogram('app_request_latency_seconds', 'Request latency in seconds')
ERROR_COUNT = Counter('app_error_count', 'Total errors')

# CPU usage metric (container)
CPU_USAGE = Gauge('cpu_usage_percent', 'CPU usage percent of this container')

@app.route('/')
def home():
    start = time.time()
    # simulate latency
    time.sleep(random.uniform(0.1, 0.5))
    # simulate errors
    if random.random() < 0.2:
        ERROR_COUNT.inc()
        return "Error!", 500
    REQUEST_COUNT.inc()
    LATENCY.observe(time.time() - start)
    return "Hello, SRE!"

@app.route('/metrics')
def metrics():
    # update CPU usage sa intervalom 0.1s
    CPU_USAGE.set(psutil.cpu_percent(interval=0.1))
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

