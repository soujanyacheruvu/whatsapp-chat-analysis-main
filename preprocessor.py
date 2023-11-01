import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    if len(messages) != len(dates):
        raise ValueError("Mismatch in the number of dates and messages.")

    df = pd.DataFrame({'message_date': dates, 'user_message': messages})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')

    df['user_message'] = df['user_message'].astype(str)
    df['user'] = df['user_message'].str.extract('([^:]+):', expand=False).fillna('group_notification')

    df['message'] = df['user_message'].str.split(': ').str[1]

    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['message_date'].dt.date
    df['year'] = df['message_date'].dt.year
    df['month_num'] = df['message_date'].dt.month
    df['month'] = df['message_date'].dt.strftime('%B')
    df['day'] = df['message_date'].dt.day
    df['day_name'] = df['message_date'].dt.strftime('%A')
    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute

    df['period'] = df['message_date'].apply(lambda x: f"{x.hour:02d}-{(x.hour + 1) % 24:02d}")

    return df

# Example usage:
data = """
10/01/2023, 14:30 - User1: Hello!
10/01/2023, 14:35 - User2: Hi there!
10/01/2023, 14:40 - User1: How are you?
"""

df = preprocess(data)
print(df)
