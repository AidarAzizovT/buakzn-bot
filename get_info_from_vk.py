import requests
import datetime


def get_data():
    gmt3 = datetime.timezone(datetime.timedelta(hours=3))
    group_name = 'buakzn'
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


def search_for_today(time, dest):
    time_range = generate_range(time)
    data = get_data()
    filtered_data = []

    for elem in data:
        if dest in elem['text'].lower(): #check where we are going
            if 'нужн' not in elem['text'].lower():
                if elem['published_date'].day == datetime.datetime.now().day:
                    for hour in time_range:
                        if hour in elem['text']:
                            filtered_data.append(elem)
                            break
    return filtered_data



def generate_range(time: str):
    time_range = []
    hour = int(time[:2])
    for delta_hour in range(hour - 2, hour + 4):
        time_range.append(str(delta_hour % 24))
    return time_range

print(search_for_today('18:00', 'в буинск'))
