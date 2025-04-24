import  pandas as pd
import  random
import datetime as dt
import smtplib
from email.mime.multipart import  MIMEMultipart
from email.mime.text import MIMEText
import base64



MY_EMAIL = "t92066369@gmail.com"
PASSWORD = "wjpmwjfafqcnqdlo"  # Replace with your App Password

today = dt.datetime.now()
data = pd.read_csv("birthdays.csv")
info = []
for index, item in data.iterrows():
    info.append([item['name'], item['email'],(item['day'], item['month'])])

def check_birthday(today_date, credentials):
    if today_date == credentials[2]:
        return True


today_tuple = (today.day, today.month)
birthday_people = []
for cred in info:
    if check_birthday(today_tuple, cred):
        birthday_people.append(cred)
if len(birthday_people) > 0:
    for person in birthday_people:
        name = person[0]
        email = person[1]
        with open(f"letter_templates/letter_{random.randint(1,3)}.txt") as file:

            data = file.read()

        cleaned_message = data.replace("[NAME]", str(name))

        message = MIMEMultipart()
        message['From'] = MY_EMAIL
        message['To'] = email
        message['Subject'] = "Happy Birthday 🎉🎉🎉"
        message.attach(MIMEText(cleaned_message,'plain'))

        filename = "birthdaycard.jpg"
        # Read and encode image as base64
        with open(filename, "rb") as img_file:
            encoded_string = base64.b64encode(img_file.read()).decode('utf-8')

        # Create HTML content with embedded image
        html = f"""
        <html>
          <body>
            <img src="data:image/jpeg;base64,{encoded_string}" alt="Cool Image" style="width:400px;">
          </body>
        </html>
        """

        message.attach(MIMEText(html,"html"))



        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:

            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=email,
                                msg=message.as_string())

day_of_the_week = today.weekday()
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


for person in info:

    with open("motivational_quotes/quotes.txt", "r") as file:
        quotes = file.readlines()

    random_quote = random.choice(quotes)
    quote = random_quote.split("-")[0].strip('" "')
    author = random_quote.split("-")[1]
    message = (f"Subject:{days[day_of_the_week]} Motivation \n\n"
               f"{quote}\n\n"
               f"--- By {author}")
    print(message)

    email = person[1]
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=email,
            msg=message
        )
