import  sqlite3       
from datetime import datetime, timezone

from config import BOT_TOKEN,SITE_TO_AUTH, SFX_SITE, DATABASES

conn = sqlite3.connect(DATABASES)
cur = conn.cursor()

username='kkkkrrrr'
msg1='ooo'
msgid='1'
token='dc8e1706-c8cb-4b66-991c-9b32c1c0bbc9'
date = datetime.now()

sql = (f"""INSERT INTO djauth_user (is_superuser,is_staff, is_active, date_joined,username,first_name,last_name,idtlg,email,token,password)
            VALUES (1,1,1,'{date}','{username}','{msg1}','{msg1}','{msgid}',
            '{msg1}','{token}','{token}');""")

# sql = (f"""INSERT INTO djauth_user (is_superuser,is_staff, is_active, date_joined,username,first_name,last_name,idtlg,email,token,password)
#             VALUES (1,1,1,{datetime.now(timezone.utc)},'{username}','{msg1}','{msg1}','{msgid}',
#             '{str(msgid)+SFX_SITE}','{token}','{token}');""")

# sql = (f"""INSERT INTO djauth_user
# (password, last_login, is_superuser, username, first_name,
#  last_name, email, is_staff, is_active, date_joined, idtlg, token)
# VALUES('jfhfwkfrfrl', NULL, 0, 'mayy', '', '', 'admin@test.com', 1, 1, '2024-12-03 15:17:30.241935', NULL, NULL);""")

cur.execute(sql)

conn.commit()
conn.close()