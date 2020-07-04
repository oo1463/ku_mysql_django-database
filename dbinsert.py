import pandas as pd
import pymysql


conn = pymysql.connect(host='localhost', user='db2020', password='db2020', db='db_201511291')
curs = conn.cursor(pymysql.cursors.DictCursor)


############################
############################

user = pd.read_csv(r"C:\Users\oooo1\Desktop\수업\20년1학기\데이터베이스\기말 과제\movielens dataset\u.user.tsv", engine='python',
                   delimiter='|', header=None)

sql = "insert into user (uid, age, gender, occup, zipcode) values (%s, %s, %s, %s, %s)"  # user insert

tmp = []
for x in user.values:
    tmp.append(tuple(x))
curs.executemany(sql, tmp)
conn.commit()

############################
############################

movie = pd.read_csv(r"C:\Users\oooo1\Desktop\수업\20년1학기\데이터베이스\기말 과제\movielens dataset\u.item.tsv", engine='python',
                     delimiter='|', header=None)


sql = "insert into movie (mid, title, r_date, v_date, url) values (%s, %s, %s, %s, %s)"  # movie insert

tmp = []
genre_list = []
genre_tuple = ()
count = 0
movie = movie.fillna('')

for x in movie.values:
    tmp.append(tuple(x[:5]))

    for genre_bit in tuple(x[5:]):
        if genre_bit == 1:
            genre_tuple = (count, x[0])
            genre_list.append(genre_tuple)  # genre_movie에 들어갈 튜플을 만든다
        count = count + 1
    count = 0
print(tmp)

curs.executemany(sql, tmp)
conn.commit()

############################
############################

genre = pd.read_csv(r"C:\Users\oooo1\Desktop\수업\20년1학기\데이터베이스\기말 과제\movielens dataset\u.genre.tsv", engine='python',
                    delimiter='|', header=None)

sql = "insert into genre (genre_name, gid) values (%s, %s)"  # genre insert

tmp = []
for x in genre.values:
    tmp.append(tuple(x))
print(tmp)

curs.executemany(sql, tmp)
conn.commit()

############################
############################

sql = "insert into genre_movie (gid, mid) values (%s, %s)"  # genre_movie insert
curs.executemany(sql, genre_list)

############################
############################


data = pd.read_csv(r"C:\Users\oooo1\Desktop\수업\20년1학기\데이터베이스\기말 과제\movielens dataset\u.data.tsv", engine='python',
                   delimiter='\t', header=None)


sql = "insert into data (uid, mid, rating, timestamp) values (%s, %s, %s, %s)"  # data insert

tmp = []

for x in data.values:
    uid = int(x[0])
    mid = int(x[1])
    rating = int(x[2])
    timestamp = int(x[3])
    tmp.append((uid, mid, rating, timestamp))
print(tmp)

curs.executemany(sql, tmp)
conn.commit()

############################
############################

curs.close()
conn.close()
