import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def get_sentiment(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    params = dict()
    params["text"] = kwargs["text"]
    params["version"] = kwargs["version"]
    params["features"] = kwargs["features"]
    params["return_analyzed_text"] = kwargs["return_analyzed_text"]
    API_KEY = "-gObtGUoQHjdlkP2hDDD1V0WJfmtc1OxaAc8Kwjdik9Y"
    try:
        response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', API_KEY))
    except:
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def post_review(url, json_payload, **kwargs):
    results = []
    json_result = post_request(url, json_payload)
    if json_result:
        print(json_result)
    return results

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    if json_result:
        dealers = json_result["body"]["rows"]
        for dealer in dealers:
            dealer_doc = dealer["doc"]
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                  id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                  short_name=dealer_doc["short_name"],
                                  st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        reviews = json_result["body"]["data"]["docs"]
        for review in reviews:
            review_obj = DealerReview(dealership=review["dealership"], name=review["name"], purchase=review["purchase"], review=review["review"], purchase_date=review["purchase_date"], car_make=review["car_make"], car_model=review["car_model"], car_year=review["car_year"], sentiment="positive", id=review["id"])
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    results = []
    API_URL = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/6b94e9ab-45c9-4ecc-98b2-8acdc352b509/v1/analyze"
    json_result = get_sentiment(API_URL, text=text, version="2020-08-01", features= "sentiment", return_analyzed_text=True)
    if json_result:
        try:
            sentiment = json_result["sentiment"]["document"]['label']
            return sentiment
        except:
            return "neutral"
    return "neutral"