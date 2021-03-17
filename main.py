from psaw import PushshiftAPI
from datetime import datetime, date, timedelta
import tkinter, yahoo_fin.stock_info as si
import webbrowser, requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

tags = []
urls = {}
line = 0

def open_url(event, tag):
    webbrowser.open(urls[tag])

def add_link(event, post):
    tag = "tag" + str(line)
    urls[tag] = post.url
    text.insert('1.0', post.title + "\n")
    text.tag_add(tag, '1.0', '1.end')
    text.tag_config(tag, foreground='blue', underline=True)
    callback = lambda even, tag = tag: open_url(event, tag)
    text.tag_bind(tag, '<Button-1>', callback)
    return line + 1

def setup_chrome():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    return webdriver.Chrome(options=chrome_options)

def when_pressed(event=None):
    global line, tags, urls

    try:
        si.get_data(tick_enter.get())
    except Exception:
        text.insert('1.0', "Invalid Ticker\n")
        return

    date_to_use = datetime.now() - timedelta(days=2)
    try:
        if date_enter.get() != "":
            date_to_use = datetime.strptime(date_enter.get(), '%m/%d/%Y')
    except Exception:
        date_to_use = datetime.now() - timedelta(days=3)

    api = PushshiftAPI()

    start = int(datetime(hour=1, month=date_to_use.month, year=date_to_use.year, day=date_to_use.day).timestamp())
    posts = api.search_submissions(q = str("$" + tick_enter.get().upper()), after=start, before = int((datetime.now() - timedelta(hours=2)).timestamp()), subreddit='wallstreetbets', filter=['url', 'title'], limit=500)
    
    for post in posts:
        words = post.title.split()
        cashtags = list(set(filter(lambda word: word.lower().startswith('$'), words)))
        if len(cashtags) > 0:
            for cashtag in cashtags:
                if ("$" + tick_enter.get().upper()) in cashtag:
                    if "www.reddit.com" in post.url:                        
                        browser = setup_chrome()
                        browser.get(post.url)

                        # searching for this div tag <div class="Nt8TnDvJ2BsL8KWcFQKy5">Sorry, this post has been removed by the moderators of r/wallstreetbets.</div>
                        try:
                            browser.find_element_by_xpath("//div[@class='Nt8TnDvJ2BsL8KWcFQKy5']")
                        except Exception:                        
                            line = add_link(event, post)
                        browser.quit()
                        break
                    
    

#This defines layout, I haven't quite figured out how to make it all fit how I want.

gui = tkinter.Tk()
main_frame = tkinter.Frame(gui)
main_frame.pack()
reddit_frame = tkinter.Frame(main_frame, height = 50)

text = tkinter.Text(reddit_frame)

gui.title("Recent Reddit Posts with Cashtags")
tick = tkinter.Label(reddit_frame, text="Ticker:")

tick_enter = tkinter.Entry(reddit_frame, width = 25)
tick_enter.bind('<Return>', when_pressed)

dat = tkinter.Label(reddit_frame, text = "Optional Date After (mm/dd/yyyy):")

date_enter = tkinter.Entry(reddit_frame, width=25)
date_enter.bind('<Return>', when_pressed)

enter_but = tkinter.Button(reddit_frame, text="Enter", command=when_pressed, height = 1, width = 10)

reddit_frame.pack(anchor='nw')
tick.pack(padx = 5, pady=5, side='top', anchor='nw')
tick_enter.place(in_=tick, relx = 1.0, x = 5, rely = 0)
dat.place(in_=tick_enter, relx = 1.0, x = 5, rely = 0)
date_enter.place(in_ = dat, relx = 1.0, x=5, rely=0)
enter_but.place(in_=date_enter, relx=1.0, x=5, rely=0)
text.pack(side='top', pady=10, fill='none')

gui.geometry("700x700")
gui.mainloop()
