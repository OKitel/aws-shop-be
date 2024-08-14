FROM python:3.12-slim

WORKDIR /bff

COPY . /bff
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3000
ENV product=https://epo4kdj6ck.execute-api.eu-central-1.amazonaws.com/prod
ENV cart=http://OKitel-cart-api-prod.eu-central-1.elasticbeanstalk.com

CMD ["gunicorn", "-b", "0.0.0.0:3000", "app:app"]