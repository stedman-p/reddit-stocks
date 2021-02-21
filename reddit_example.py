from psaw import PushshiftAPI
from datetime import datetime, date
import tkinter

def when_pressed(event=None):
    global t, x

    api = PushshiftAPI()

    start = date.today()
    
    posts = list(api.search_submissions(after=start, subreddit='wallstreetbets', filter=['url', 'author', 'title', 'subreddit'], limit=500))

    for post in posts:
        words = post.title.split()
        cashtags = list(set(filter(lambda word: word.lower().startswith('$'), words)))
        if len(cashtags) > 0:
            for cashtag in cashtags:
                if ("$" + e.get().upper()) in cashtag:
                    t.insert('1.0', post.title + "\n")
                    t.insert('2.0', post.url + "\n")
                    x = x + 2
                    break


x = 0

gui = tkinter.Tk()
t = tkinter.Text(gui)

gui.title("Recent Reddit Posts with Cashtags")
l = tkinter.Label(gui, text="Enter the ticker symbol:")

e = tkinter.Entry(gui, width = 25)
e.bind('<Return>', when_pressed)
b = tkinter.Button(gui, text="Enter", command=when_pressed, height = 1, width = 10)
l.pack()
t.pack(side='bottom')
e.pack(side="left")
b.pack(side="left")
gui.mainloop()
