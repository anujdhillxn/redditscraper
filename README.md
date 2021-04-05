## Create a reddit account!
- Signup for a reddit account.
- Select the "Are you a developer? Create an app button" <a href="https://reddit.com/prefs/apps"  target="_blank">Here</a>.
- Give you program a name and a redirect URL(http://<span></span>localhost).
- On the final screen note your client id and secret.

| Create Account | Access Developer | Name | ID and secret |
| --- | --- | --- | --- |
| <img src="https://i.imgur.com/l5tWhOW.png" title="source: imgur.com" width="200" height="200" /> | <img src="https://i.imgur.com/Ir7Nqx6.png" title="source: imgur.com" width="200" height="200" /> | <img src="https://i.imgur.com/1hoKGvH.png" title="source: imgur.com" width="200" height="200" /> | <img src="https://i.imgur.com/JmH5vBn.png" title="source: imgur.com" width="200" height="200" /> |

## Run download script!
- Add any subs you want to download to the sub_list.csv one per line.
- Run SubDownload.py
- The first time you run the script it will ask you for details. Note you don't need to enter a user name or password if you don't plan on posting.
- The script will create a token.pickle file so you don't have to enter them again. If you mess up your credentials just delete the pickle file and it will ask for them again.
- The script will create an images folder and a videos folder and fill them with images and videos respectively. You can change how many posts it checks on each subreddit by changing limit for each subreddit in sub_list.csv.
- A database is also maintained for all the images and videos downloaded so far. For now, the title and author name is stored for each file in "posted.csv". You can modify the script to store more items.
- Each file downloaded has a unique ID which is used to check if the file is already present in the database. If it is, then the file is not downloaded again.
- For fast searching, a trie made of only the unique IDs is used. It can be serialized and deserialized for future usage.