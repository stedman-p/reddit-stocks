from psaw import PushshiftAPI
from datetime import datetime, date, timedelta
import tkinter
import webbrowser

tags = []
urls = {}

def show_hand_cursor(event):
    text.config(cursor='arrow')

def show_xterm_cursor(event):
    text.config(cursor='xterm')

def do(event, tag):
    
    webbrowser.open(urls[tag])
    

def when_pressed(event=None):
    global x, tags, urls

    api = PushshiftAPI()
    now = datetime.now() - timedelta(days=3)
    start = datetime(hour=1, month=now.month, year=now.year, day=now.day)
    posts = list(api.search_submissions(after=start, subreddit='wallstreetbets', filter=['url', 'author', 'title', 'subreddit'], limit=1000))

    for post in posts:
        words = post.title.split()
        cashtags = list(set(filter(lambda word: word.lower().startswith('$'), words)))
        if len(cashtags) > 0:
            for cashtag in cashtags:
                if ("$" + e.get().upper()) in cashtag:
                    print(post.url)
                    urls["tag"+str(x)] = post.url
                    text.insert('1.0', post.title + "\n")
                    text.tag_add("tag"+str(x), '1.0', '1.end')
                    text.tag_config("tag"+str(x), foreground='blue', underline=True)
                    text.tag_bind("tag"+str(x), '<Enter>', show_hand_cursor)
                    text.tag_bind("tag"+str(x), '<Leave>', show_xterm_cursor)
                    tag = "tag" + str(x)
                    callback = lambda even, tag=tag: do(event, tag)
                    text.tag_bind("tag"+str(x), '<Button-1>', callback)
                    x = x + 1
                    break


x = 0

gui = tkinter.Tk()
text = tkinter.Text(gui)
#date = tkinter.Text(gui)
gui.title("Recent Reddit Posts with Cashtags")
l = tkinter.Label(gui, text="Ticker:")

e = tkinter.Entry(gui, width = 25)
e.bind('<Return>', when_pressed)
b = tkinter.Button(gui, text="Enter", command=when_pressed, height = 1, width = 10)

# add all elements to the gui
text.pack(side='bottom')
l.pack(side='left')
e.pack(side="left")
b.pack(side="left")
gui.mainloop()
