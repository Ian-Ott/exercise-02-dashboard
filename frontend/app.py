"""
Exercise 02 — Streamlit Dashboard

Implement a Streamlit frontend that consumes the Node Registry API.

The dashboard must:
- Display a table of all registered nodes (GET /api/nodes from the API)
- Show a form to register a new node (POST /api/nodes)
- Allow deleting a node by name (DELETE /api/nodes/{name})
- Show a health status indicator (GET /health)

The API runs at the URL in the API_URL environment variable (default: http://api:8080).
"""

# TODO: Implement your Streamlit dashboard here


from flask import Flask, request, redirect
import requests
import os

app = Flask(__name__)

API_URL = os.getenv("API_URL", "http://api:8080")


@app.route("/", methods=["GET"])
def index():

    # -------------------------
    # GET NODES
    # -------------------------

    try:

        response = requests.get(f"{API_URL}/api/nodes")

        if response.status_code == 200:
            nodes = response.json()
        else:
            nodes = []

    except:
        nodes = []

    # -------------------------
    # HEALTH
    # -------------------------

    try:

        health_response = requests.get(f"{API_URL}/health")

        if health_response.status_code == 200:
            health_status = "Healthy"
        else:
            health_status = "Unhealthy"

    except:
        health_status = "Unavailable"

    html = f"""
    <html>

    <head>
        <title>Node Registry Dashboard</title>
    </head>

    <body>

        <h1>Nodes</h1>

        <table border="1">

            <tr>
                <th>Name</th>
                <th>Host</th>
                <th>Port</th>
                <th>Status</th>
            </tr>
    """

    for node in nodes:

        html += f"""
            <tr>
                <td>{node.get("name")}</td>
                <td>{node.get("host")}</td>
                <td>{node.get("port")}</td>
                <td>{node.get("status")}</td>
            </tr>
        """

    html += f"""
        </table>

        <h1>Register</h1>

        <form action="/register" method="post">

            <input
                type="text"
                name="name"
                placeholder="Name"
                required
            >

            <input
                type="text"
                name="host"
                placeholder="Host"
                required
            >

            <input
                type="number"
                name="port"
                placeholder="Port"
                required
            >

            <button type="submit">
                Register
            </button>

        </form>

        <h1>Delete Node</h1>

        <form action="/delete" method="post">

            <input
                type="text"
                name="name"
                placeholder="Node name"
                required
            >

            <button type="submit">
                Delete
            </button>

        </form>

        <h1>Health</h1>

        <p>
            API Status: {health_status}
        </p>

    </body>

    </html>
    """

    return html


@app.route("/register", methods=["POST"])
def register():

    payload = {
        "name": request.form["name"],
        "host": request.form["host"],
        "port": int(request.form["port"])
    }

    requests.post(
        f"{API_URL}/api/nodes",
        json=payload
    )

    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():

    node_name = request.form["name"]

    requests.delete(
        f"{API_URL}/api/nodes/{node_name}"
    )

    return redirect("/")


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8501
    )