from psaw import PushshiftAPI
import datetime
import tkinter

gui = tkinter.Tk()

x = 0
y = 0
api = PushshiftAPI()

start = int(datetime.datetime(2020,2,15).timestamp())

posts = api.search_submissions(after=start, subreddit='wallstreetbets', filter=['url', 'author', 'title', 'subreddit'], limit=100)

for post in posts:
    words = post.title.split()
    cashtags = list(set(filter(lambda word: word.lower().startswith('$'), words)))
    if len(cashtags) > 0:
        for cashtag in cashtags:
            tkinter.Label(gui, text=(cashtag + "\n"), font = ("Times New Roman", 12)).place(x=x, y=y)
            y = y + 20

gui.geometry("400x400")
gui.title("Recent Reddit Posts with Cashtags")
gui.mainloop()