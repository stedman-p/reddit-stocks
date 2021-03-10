from psaw import PushshiftAPI
from datetime import datetime, date, timedelta
import tkinter
import webbrowser, requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

tags = []
urls = {}

def do(event, tag):
    
    webbrowser.open(urls[tag])
    

def when_pressed(event=None):
    global x, tags, urls

    api = PushshiftAPI()
    date_to_use = datetime.now() - timedelta(days=3)
    if date_enter.get() != "":
        date_to_use = datetime.strptime(date_enter.get(), '%m/%d/%Y')
    start = datetime(hour=1, month=date_to_use.month, year=date_to_use.year, day=date_to_use.day)
    posts = list(api.search_submissions(q = str(tick_enter.get().upper()), after=start, subreddit='wallstreetbets', filter=['url', 'title',], limit=500))

    for post in posts:
        words = post.title.split()
        cashtags = list(set(filter(lambda word: word.lower().startswith('$'), words)))
        if len(cashtags) > 0:
            for cashtag in cashtags:
                if ("$" + tick_enter.get().upper()) in cashtag:
                    if "www.reddit.com" in post.url:
                        #print(post.url)
                        chrome_options = Options()
                        chrome_options.add_argument("--headless")
                        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
                        browser = webdriver.Chrome(options=chrome_options)
                        browser.get(post.url)
                        try:
                            browser.find_element_by_xpath("//div[@class='Nt8TnDvJ2BsL8KWcFQKy5']")
                        except:                        
                            urls["tag"+str(x)] = post.url
                            text.insert('1.0', post.title + "\n")
                            text.tag_add("tag"+str(x), '1.0', '1.end')
                            text.tag_config("tag"+str(x), foreground='blue', underline=True)
                            tag = "tag" + str(x)
                            callback = lambda even, tag=tag: do(event, tag)
                            text.tag_bind("tag"+str(x), '<Button-1>', callback)
                            x = x + 1
                        browser.quit()
                        break
                    #class="Nt8TnDvJ2BsL8KWcFQKy5">Sorry, this post has been removed by the moderators of r/wallstreetbets.</div>
    
x = 0

gui = tkinter.Tk()
text = tkinter.Text(gui)
#date = tkinter.Text(gui)
gui.title("Recent Reddit Posts with Cashtags")
tick = tkinter.Label(gui, text="Ticker:")

tick_enter = tkinter.Entry(gui, width = 25)
tick_enter.bind('<Return>', when_pressed)

dat = tkinter.Label(gui, text = "Date After (mm/dd/yyyy):")

date_enter = tkinter.Entry(gui, width=25)
date_enter.bind('<Return>', when_pressed)

enter_but = tkinter.Button(gui, text="Enter", command=when_pressed, height = 1, width = 10)

text.pack(side='bottom')
tick.pack(side='left')
tick_enter.pack(side="left")
dat.pack(side='left')
date_enter.pack(side='left')
enter_but.pack(side="left")
gui.mainloop()
