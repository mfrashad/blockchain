FROM python:3.6-alpine

WORKDIR /app

# Install dependencies.
ADD requirements.txt /app
RUN cd /app && \
    pip install -r requirements.txt

# Add actual source code.
ADD pow_app.py /app

EXPOSE 5001

CMD ["python", "pow_app.py", "--port", "5001"]
