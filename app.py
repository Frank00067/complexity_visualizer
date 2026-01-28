from flask import Flask, request, jsonify
import time
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for server
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# ----- Algorithms -----
def linear_search(n):
    for i in range(n):
        if i == n-1:
            return i

def bubble_sort(n):
    arr = np.random.randint(0, 100, n)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def binary_search(n):
    arr = sorted(np.random.randint(0, 100, n))
    target = arr[-1]
    left, right = 0, n - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def nested_loops(n):
    count = 0
    for i in range(n):
        for j in range(n):
            count += 1
    return count

ALGO_MAP = {
    "bubble": bubble_sort,
    "linear": linear_search,
    "binary": binary_search,
    "nested": nested_loops
}

# ----- Analyze Endpoint -----
@app.route("/analyze")
def analyze():
    algo_name = request.args.get("algo", "bubble").lower()
    n = int(request.args.get("n", 100))
    steps = int(request.args.get("steps", 10))

    if algo_name not in ALGO_MAP:
        return jsonify({"error": "Invalid algorithm"}), 400

    algo_func = ALGO_MAP[algo_name]

    n_values = []
    times = []

    for step in range(1, steps+1):
        current_n = int(n * step / steps)
        start_time = time.time()
        algo_func(current_n)
        end_time = time.time()
        n_values.append(current_n)
        times.append(end_time - start_time)

    # ----- Create Graph -----
    plt.figure()
    plt.plot(n_values, times, 'o-', color='blue')
    plt.title(f"{algo_name.capitalize()} Performance")
    plt.xlabel("n (Elements)")
    plt.ylabel("Time (seconds)")
    plt.grid(True)

    # Save graph to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')

    # ----- Save as PNG locally automatically -----
    with open("graph.png", "wb") as f:
        f.write(base64.b64decode(img_base64))

    print("Graph saved as graph.png!")

    # ----- Respond JSON -----
    response = {
        "algorithm": algo_name,
        "n": n,
        "steps": steps,
        "n_values": n_values,
        "times": times,
        "total_time": sum(times),
        "graph_base64": img_base64
    }

    return jsonify(response)

if __name__ == "__main__":
    print("Flask server running on http://localhost:3000")
    print("Access /analyze?algo=bubble&n=1000&steps=10")
    app.run(port=3000, debug=True)
