import smtplib
import time

import requests
from datetime import datetime

MY_LAT = 34.0522                # Your latitude
MY_LONG = 118.2437              # Your longitude
MAIL = "testemail@gmail.com"    # Your EMail ID
PASSWORD = "test"               # Your Password
OFFSET = 2                      # The offset (time difference) between your timezone and UTC

def in_position():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = float(data["results"]["sunrise"].split("T")[1].split(":")[0]) + OFFSET
    sunset = float(data["results"]["sunset"].split("T")[1].split(":")[0]) + OFFSET

    time_now = (datetime.now().hour)

    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if in_position() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com", 587)
        connection.starttls()
        connection.login(MAIL, PASSWORD)
        connection.sendmail(
            from_addr=MAIL,
            to_addrs=MAIL,
            msg="Subject:Look Up!\n\nThe ISS is above you in the sky."
        )
