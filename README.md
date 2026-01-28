# Algorithm Analysis Flask App

A simple Flask API that analyzes algorithm performance and returns execution times plus a Base64 graph image.

## Install

```bash
pip install flask matplotlib numpy
```

## Run

```bash
python3 server.py
```

App runs at:

```
http://localhost:3000
```

## Endpoint

```
/analyze?algo=bubble&n=1000&steps=10
```

**Params:**

* `algo`: bubble | linear | binary | nested
* `n`: input size
* `steps`: step size

## Graph

The response includes a Base64 image. Decode it to get the graph.
# complexity_visualizer
