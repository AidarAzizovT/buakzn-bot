import requests
import datetime
from config import TOKEN_VK


groups_name = ['buakzn', 'bua_777_kazan', 'nampoputi1']
def get_data(group_name = 'buakzn'):
    gmt3 = datetime.timezone(datetime.timedelta(hours=3))
    url = f"https://api.vk.com/method/wall.get?domain={group_name}&access_token={TOKEN_VK}&v=5.131&count=40"
    response = requests.get(url).json()['response']['items']

    data = []
    for elem in response:
        link_to_publisher = f'https://vk.com/id{elem["from_id"]}'
        date_of_publishing = datetime.datetime.fromtimestamp(elem["date"])
        date_of_publishing = date_of_publishing.astimezone(gmt3)
        text = elem["text"]
        data.append({"link_to_publisher": link_to_publisher, "published_date": date_of_publishing, "text": text})

    return data


def search_for_today_passenger(time, dest):
    time_range = generate_range(time)
    data = get_multiple_groups_posts()

    filtered_data = []

    for elem in data:
        if dest in elem['text'].lower(): #check where we are going
            if 'нужн' not in elem['text'].lower() and 'завтра' not in elem['text'].lower():
                if elem['published_date'].day == datetime.datetime.now().day:
                    for hour in time_range:
                        if hour in elem['text']:
                            filtered_data.append(elem)
                            break
    return filtered_data


def search_for_tommorow_passenger(time, dest):
    time_range = generate_range(time)
    data = get_multiple_groups_posts()
    filtered_data = []

    for elem in data:
        if dest in elem['text'].lower():  # check where we are going
            if ('нужн' not in elem['text'].lower()) and ('завтра' in elem['text'].lower()):
                if elem['published_date'].day == datetime.datetime.now().day:
                    for hour in time_range:
                        if hour in elem['text']:
                            filtered_data.append(elem)
                            break
    return filtered_data


def search_for_today_driver(time, dest):
    time_range = generate_range(time)
    data = get_multiple_groups_posts()

    filtered_data = []

    for elem in data:
        if dest in elem['text'].lower(): #check where we are going
            if 'нужн' in elem['text'].lower() and 'завтра' not in elem['text'].lower():
                if elem['published_date'].day == datetime.datetime.now().day:
                    for hour in time_range:
                        if hour in elem['text']:
                            filtered_data.append(elem)
                            break
    return filtered_data


def search_for_tommorow_driver(time, dest):
    time_range = generate_range(time)
    data = get_multiple_groups_posts()
    filtered_data = []

    for elem in data:
        if dest in elem['text'].lower():  # check where we are going
            if ('нужн' in elem['text'].lower()) and ('завтра' in elem['text'].lower()):
                if elem['published_date'].day == datetime.datetime.now().day:
                    for hour in time_range:
                        if hour in elem['text']:
                            filtered_data.append(elem)
                            break

def generate_range(time: str):
    time_range = []
    hour = int(time[:2])
    for delta_hour in range(hour - 2, hour + 4):
        time_range.append(f'{str(delta_hour % 24)}:')
        time_range.append(f'{str(delta_hour % 24)}.')

    return time_range


def get_multiple_groups_posts():
    sum_of_groupsposts = []
    for group_name in groups_name:
        sum_of_groupsposts += get_data(group_name)
        print(len(sum_of_groupsposts))
    return sum_of_groupsposts



