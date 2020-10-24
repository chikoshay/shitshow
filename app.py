import os

from flask import Flask, render_template, request

import holidayapi


app = Flask(__name__)

KEY = os.getenv('HOLIDAY_KEY')
hapi = holidayapi.v1(KEY)


def get_api(month, day, country):
    parameters = {
        'country': country,
        'year': 2019,
        # since it's a free version i've added the only available year
        'month': month,
        'day': day,
    }

    holidays = hapi.holidays(parameters)
    return holidays


def check_holiday(holidays):
    event = "regular day"
    if 'holidays' in holidays:
        if len(holidays.get('holidays')) > 0:
            event = holidays.get('holidays')[0].get("name")
        return event


def get_day(user_date):
    date_list = user_date.split("-")
    day = date_list[2]
    return int(day)


def get_month(user_date):
    date_list = user_date.split("-")
    month = date_list[1]
    return int(month)


def wordsmith(event, country):
    if event == "regular day":
        headline_status = "DAY!"
        verdict = "I LOVE WHEN A GOOD PLAN COMES TOGETHER"
        holishit_result = "Lucky you! For the locals it's just a dull day!"
    elif event is None:
        headline_status = "Huston, we have a problem"
        verdict = "Our engin is broken"
        holishit_result = "It's probably a KEY issue. come back later"
    else:
        headline_status = "SHIT!"
        verdict = f"For the {country} folks it's {event}"
        holishit_result = "Everything is closed. You need to find a new date."
    return headline_status, verdict, holishit_result


@app.route("/", methods=["GET", "POST"])
def shit():
    event = "Try us..."
    if request.method == "GET":
        try:
            departure = request.args.getlist("departure")[0]
            country = request.args.getlist("country")[0]
            depart_day = get_day(departure)
            depart_month = get_month(departure)
            holidays = get_api(depart_month, depart_day, country)
            event = check_holiday(holidays)
            headline_status, what_is_happaning, what_to_do = wordsmith(
                event, country)
        except IndexError:
            event = "Try us... error"
            headline_status = "Choose date"
            what_is_happaning = "Choose country"
            what_to_do = "Choose Life"
    return render_template("index.j2",
                           status=headline_status,
                           verdict=what_is_happaning,
                           holishit_result=what_to_do,
                           )


if __name__ == "__main__":
    app.run(debug=False)