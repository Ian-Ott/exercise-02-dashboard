# TODO: Write Dockerfile for the Streamlit frontend
#
# Requirements:
# - Base image: python:3.14-slim (pinned, no :latest)
# - Install dependencies from requirements.txt
# - Non-root USER
# - EXPOSE 8501
# - Start: streamlit run app.py --server.port=8501 --server.address=0.0.0.0

FROM python:3.14-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.14-slim
WORKDIR /app
COPY --from=builder /install /usr/local
RUN useradd -m appuser
USER appuser
COPY app.py .
EXPOSE 8501
CMD ["python","app.py"]
