import requests
import bs4
import collections

weather_report = collections.namedtuple('weather_report', 'location, temperature')


def main():
    print_header()
    city = get_city().lower()
    state = get_state().lower()
    html = get_html_from_web(state, city)
    weather = get_weather_from_html(html)
    display_weather(weather)


def print_header():
    print('------------------------------')
    print('         WEATHER APP')
    print('------------------------------')
    print()


def get_city():
    return input('Enter city (Englewood): ')


def get_state():
    return input('Enter US state (CO): ')


def get_html_from_web(state, city):
    url = 'https://www.wunderground.com/weather/us/{}/{}'.format(
        state, city)
    response = requests.get(url)
    return response.text


def get_weather_from_html(html):
    # cityCss = 'h1'
    # weatherScaleCss = '.wu-unit-temperature .wu-label'
    # weatherTempCss = '.wu-unit-temperature .wu-value'
    # weatherConditionCss = '.condition-icon'

    soup = bs4.BeautifulSoup(html, 'html.parser')
    loc = soup.find('h1').get_text(strip=True)  \
        .replace(' Weather Conditions', '') \
        .replace('star_ratehome', '')
    temp = soup.find(attrs={"class":"wu-unit-temperature"}).get_text(strip=True)
    loc = clean_text(loc)
    temp = clean_text(temp)
    report = weather_report(location=loc, temperature=temp)
    return report
       

def clean_text(text):
    if text:
        text = text.strip()
    return text


def display_weather(weather):
    print("Location: {} Temperature: {}".format(weather.location, weather.temperature))  


if __name__ == '__main__':
    main()
