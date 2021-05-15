import requests
import json
import sqlite3

url = 'https://ghibliapi.herokuapp.com/films'

# 1.1 request მოდულის ფუნქცია
r = requests.get(url)

# 1.2 request მოდულის ფუნქცია
res = r.json()

# 1.3 request მოდულის ფუნქცია
# აქ უბრალოდ ვერ მოვიფიქრე request მოდულიდან კიდევ რა შეიძლებოდა გამომეყენებინა და უბრალოდ კონტენტის ტიპი დავპრინტე :დ
print(r.headers['content-type'])

# 2 json ფაილი
ordered_res = json.dumps(res, indent=4)

with open("ghibli.json", "w") as f:
    f.write(ordered_res)


# 4 ბაზები
conn = sqlite3.connect("ghibli.sqlite")
cursor = conn.cursor()
# cursor.execute('''CREATE TABLE ghibli (id INTEGER PRIMARY KEY AUTOINCREMENT, title VARCHAR(50), description VARCHAR(500),
#               director VARCHAR(30), release_date VARCHAR(10), run_time INT);''')

input_title = input("Search anime by title: ")

i = 0
while i < len(res):
    title = res[i]['title']
    desc = res[i]['description']
    dir = res[i]['director']
    rel_date = res[i]['release_date']
    run_time = res[i]['running_time']
    info = (title, desc, dir, rel_date, run_time)
    cursor.execute("INSERT INTO ghibli (title, description, director, release_date, run_time) VALUES (?, ?, ?, ?, ?)",
                   info)
    conn.commit()

    # 3 მომხმარებელს შეყავს ანიმეს სახელი და შესაბამისად გამოაქვს მასზე ინფორმაცია
    # ანიმეებში რომ ვერ ერკვეოდეთ და სათაურების მოძებნა არ დაჭირდეთ, აქვე ჩამოვწერ ზოგს :დდ
    # My Neighbor Totoro, Princess Mononoke, Spirited Away, Howl's Moving Castle, Grave of the Fireflies...

    if input_title.upper() == title.upper():
        print("სათაური: ", title, '\nაღწერა: ', desc, '\n რეჟისორი: ', dir, '\nგამოშვების თარიღი: ', rel_date,
              '\nხანგძლივობა: ', run_time)

    i += 1


conn.close()
f.close()
