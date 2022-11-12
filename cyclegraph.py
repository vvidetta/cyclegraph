import argparse
import requests
import json

from datetime import datetime
from config import email, password, client_id

def parse_args():
  parser = argparse.ArgumentParser(description='Display graph of cumulative distance cycled over time')
  parser.add_argument('start_date', type=str,
                      help='Start date')
  parser.add_argument('end_date', type=str,
                      help='End date')

  args = parser.parse_args()
  return args.start_date, args.end_date

def parse_dates(start: str, end: str) -> tuple:
  start_date = datetime.fromisoformat(start)
  end_date = datetime.fromisoformat(end)
  return start_date, end_date

if __name__ == '__main__':
  # start, end = parse_args()
  # start_date, end_date = parse_dates(start, end)
  # print(f'Starting on {start_date}, end on {end_date}')

  login_url = "https://account.komoot.com/v1/signin"
  tour_url = f"https://www.komoot.com/user/{client_id}/tours"

  # Create a session to store login data
  s = requests.Session()
  
  # Get the login page and save the cookies
  res = requests.get(login_url)
  cookies = res.cookies.get_dict()
  
  # Create request headers dictionary
  headers = {
      "Content-Type": "application/json"
  }
  
  # Populate request body with credentials
  payload = json.dumps({
      "email": email,
      "password": password,
      "reason": "null"
  })
  
  # POST request
  s.post(login_url, headers=headers,
            data=payload, cookies=cookies)

  url = "https://account.komoot.com/actions/transfer?type=signin"
  s.get(url)

  headers = {"onlyprops": "true"}

  response = s.get(tour_url, headers=headers)
  if response.status_code != 200:
    print("Something went wrong...")
    exit(1)
  data = response.json()

  #with open("data.json", "w") as file:
  #  file.write(json.dumps(data))

  next_url = data["kmtx"]["session"]["_embedded"]["profile"] \
            ["_embedded"]["tours"]["_links"]["next"]["href"]
  response = s.get(next_url, headers=headers)
  if response.status_code != 200:
    print(f"Something went wrong... Error {response.status_code}")
    exit(1)
  data = response.json()

  with open("data.json", "w") as file:
    file.write(json.dumps(data))

  #tours = data["kmtx"]["session"]["_embedded"]["profile"] \
  #          ["_embedded"]["tours"]["_embedded"]["items"]
            #data["user"]["_embedded"]["tours"]["_embedded"]["items"]

  # records = []
  # for tour in tours:
  #   records.append({
  #     "date": tour["date"],
  #     "distance": tour["distance"]
  #   })

  # with open("distances.csv", "w") as file:
  #   for record in records:
  #     file.write(f"{record['date']}, {record['distance']}\n")

  #with open("tours.json", "w") as file:
  #  raw_json = json.dumps(tours)
  #  file.write(raw_json)
  #tours = data["kmtx"]["session"]["_embedded"]["profile"] \
  #           ["_embedded"]["tours"]["_embedded"]["items"]
  # print(tours)
