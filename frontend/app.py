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

import os
import requests
import streamlit as st


API_URL = os.getenv("API_URL", "http://api:8080")

st.title("Streamlit Dashboard")


st.header("API ALL Nodes")
try:
    response = requests.get(f"{API_URL}/api/nodes")

    if response.status_code == 200:
        nodes = response.json()
        if nodes:
            st.table(nodes)
        else:
            st.info("No nodes registered")
    else: 
        st.error("Failed to fetch nodes")
except Exception as e:
    st.error(f"Error fetching nodes: {e}")


st.header("Register new Node")
with st.form("register_node_form"):

    name = st.text_input("Name")
    host = st.text_input("Host")
    port = st.number_input("Port", min_value=1, max_value=65535, value=8080)

    submitted = st.form_submit_button("Register")

    if submitted:

        payload = {
            "name": name,
            "host": host,
            "port": port
        }

        try:
            response = requests.post(
                f"{API_URL}/api/nodes",
                json=payload
            )

            if response.status_code in [200, 201]:
                st.success("Node registered")
            else:
                st.error(response.text)

        except Exception as e:
            st.error(f"Error registering node: {e}")


st.header("Delete Node")
node_name = st.text_input("Node name to delete")
if st.button("Delete Node"):

    try:
        response = requests.delete(
            f"{API_URL}/api/nodes/{node_name}"
        )

        if response.status_code == 200:
            st.success("Node deleted")
        else:
            st.error(response.text)

    except Exception as e:
        st.error(f"Error deleting node: {e}")


st.header("API Health")
try:
    health_response = requests.get(f"{API_URL}/health")

    if health_response.status_code == 200:
        st.success("API is healthy")
    else:
        st.error("API is unhealthy")

except Exception as e:
    st.error(f"Cannot connect to API: {e}")