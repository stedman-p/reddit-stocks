from psaw import PushshiftAPI
from datetime import datetime, date, timedelta
import tkinter, yahoo_fin.stock_info as si
import webbrowser, requests, time, math
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

def datePlusOne(string):
	date = datetime.strptime(string, '%b %d, %Y')
	addOne = timedelta(days = 1)
	date = date + addOne
	strDate = date.strftime('%b %d, %Y')
	return strDate


def add_financial_info(ticker):
    current_price = float(si.get_live_price(ticker))
    info = si.get_quote_table(ticker)
    valuation = si.get_stats_valuation(ticker)
    stats = si.get_stats(ticker)
    price.config(text = "${:.2f}".format(current_price))
    close_price = float(info["Previous Close"])
    price_change = (current_price - close_price)
    percent_change = (price_change/close_price)*100
    if price_change < 0:
        color = "red"
        sign = "-"
    else: 
        color = "green"
        sign = "+"
    change.config(text = "{}${:.2f} ({}{:.2f}%)".format(sign, abs(price_change), sign, abs(percent_change)), fg = color)
    value.config(text = info["Market Cap"])

    div = info["Forward Dividend & Yield"]
    if div == "N/A (N/A)":
        dividend.configure(text = "No Dividend")
        ex_div.config(text = "No Dividend")
        payout_ratio.config(text = "No Dividend")
    else:
        dividend.config(text = "${}".format(div))
        ex_div.config(text = info["Ex-Dividend Date"])
    
    
    pe = info["PE Ratio (TTM)"]
    if str(pe) == "nan":
        pe_ratio.config(text = "Not Profitable")
        payout_ratio.config(text = "Not Profitable")
    else:
        pe_ratio.config(text = pe)
        if not payout_ratio["text"] == "No Dividend":
            payout_ratio.config(text = stats["Value"][23])

    stock_beta = info["Beta (5Y Monthly)"]
    if str(stock_beta) == "nan":
        beta.config(text = "Not enough data")
    else:
        beta.config(text = stock_beta)
    
    range_52 = info["52 Week Range"]
    range_52 = range_52.split("-")
    high_52.config(text = "${}".format(range_52[1].strip()))
    low_52.config(text = "${}".format(range_52[0].strip()))

    fwdpe = valuation[list(valuation)[1]][3]
    if str(fwdpe) == "nan":
        pe_fwd.config(text = "Not Profitable")
    else:
        pe_fwd.config(text = fwdpe)
    
    next_earn.config(text = info["Earnings Date"].split("-")[0].strip())

    
def when_pressed(event=None):
    global line, tags, urls

    text.delete('1.0', 'end')
    time.sleep(1)
    ticker = tick_enter.get().upper()
    try:
        si.get_data(ticker)
    except Exception:
        text.insert('1.0', "Invalid Ticker\n")
        return
    add_financial_info(ticker)
    
    date_to_use = datetime.now() - timedelta(days=20)
    try:
        if date_enter.get() != "":
            date_to_use = datetime.strptime(date_enter.get(), '%m/%d/%Y')
    except Exception:
        date_to_use = datetime.now() - timedelta(days=20)

    api = PushshiftAPI()
    #q = str("$" + ticker), 
    start = int(datetime(hour=1, month=date_to_use.month, year=date_to_use.year, day=date_to_use.day).timestamp())
    posts = api.search_submissions(title=str("$"+ticker),after=start, before = int((datetime.now() - timedelta(hours=2)).timestamp()), subreddit='wallstreetbets', filter=['url', 'title'], limit=1000)
    
    for post in posts:
        words = post.title.split()
        #cashtags = list(set(filter(lambda word: word.startswith('$' + ticker), words)))
        cashtags = [word for word in words if ('$' + ticker) in word]
        #        cashtags = list(set(filter(lambda word: word.lower().startswith('$' + ticker.lower(), words)))
        
        if len(cashtags) > 0:
            
            if "www.reddit.com" in post.url:                        
                browser = setup_chrome()
                browser.get(post.url)

                # searching for this div tag <div class="Nt8TnDvJ2BsL8KWcFQKy5">Sorry, this post has been removed by the moderators of r/wallstreetbets.</div>
                try:
                    browser.find_element_by_xpath("//div[@class='Nt8TnDvJ2BsL8KWcFQKy5']")
                except Exception:                        
                    line = add_link(event, post)
                browser.quit()
                    
    

#This defines layout, I haven't quite figured out how to make it all fit how I want.


gui = tkinter.Tk()
main_frame = tkinter.Frame(gui)
main_frame.pack()
reddit_frame = tkinter.Frame(gui)
reddit_frame.pack()
text = tkinter.Text(reddit_frame, height = 20)
text.pack()
info = tkinter.Label(reddit_frame, text = "Financial Information", font = ("TkDefaultFont", 15)).pack()
gui.title("Recent Reddit Posts with Cashtags")
tick = tkinter.Label(main_frame, text="Ticker:")
tick.pack(side="left")
tick_enter = tkinter.Entry(main_frame, width = 25)
tick_enter.bind('<Return>', when_pressed)
tick_enter.pack(side="left")

dat = tkinter.Label(main_frame, text = "Optional Date After (mm/dd/yyyy):")
dat.pack(side="left")
date_enter = tkinter.Entry(main_frame, width=25)
date_enter.bind('<Return>', when_pressed)
date_enter.pack(side="left")
enter_but = tkinter.Button(main_frame, text="Enter", command=when_pressed, height = 1, width = 10)
enter_but.pack(side="left")

financial_frame = tkinter.Frame(gui)
financial_frame.pack()

price_lab = tkinter.Label(financial_frame, text = "Last Price:", width = 15, anchor = "w")
price_lab.grid(row=0,column=0)
price = tkinter.Label(financial_frame, width = 15, anchor = "w")
price.grid(row = 0, column=1)
change_lab = tkinter.Label(financial_frame, text = "Day Change (%):", width = 15, anchor = "w")
change_lab.grid(row=0, column = 2)
change = tkinter.Label(financial_frame, width = 15, anchor = "w")
change.grid(row = 0, column = 3)
value_lab = tkinter.Label(financial_frame, text = "Market Cap:", width = 15, anchor = "w")
value_lab.grid(row = 0, column = 4)
value = tkinter.Label(financial_frame, width = 15, anchor = "w")
value.grid(row = 0, column = 5)
div_lab = tkinter.Label(financial_frame, text = "Dividend (Yield):", width = 15, anchor = "w")
div_lab.grid(row = 2, column = 0)
dividend = tkinter.Label(financial_frame, width = 15, anchor = "w")
dividend.grid(row = 2, column = 1)
pe_label = tkinter.Label(financial_frame, text = "P/E Ratio (TTM):", width = 15, anchor = "w")
pe_label.grid(row = 3, column = 0)
pe_ratio = tkinter.Label(financial_frame, width = 15, anchor = "w")
pe_ratio.grid(row = 3, column = 1)
beta_label = tkinter.Label(financial_frame, width = 15, anchor = "w", text = "Beta (5Y Monthly):")
beta_label.grid(row = 1, column = 4)
beta = tkinter.Label(financial_frame, width = 15, anchor = "w")
beta.grid(row = 1, column = 5)
high_52_lab = tkinter.Label(financial_frame, width = 15, anchor = "w", text = "52 Week High:")
high_52_lab.grid(row = 1, column = 0)
high_52 = tkinter.Label(financial_frame, width = 15, anchor = "w")
high_52.grid(row = 1, column = 1)
low_52_lab = tkinter.Label(financial_frame, width = 15, anchor = "w", text = "52 Week Low:")
low_52_lab.grid(row = 1, column = 2)
low_52 = tkinter.Label(financial_frame, width = 15, anchor = "w")
low_52.grid(row = 1, column = 3)
payout_ratio_lab = tkinter.Label(financial_frame, width = 15, anchor = "w", text = "Payout Ratio (TTM):")
payout_ratio_lab.grid(row = 2, column = 2)
payout_ratio = tkinter.Label(financial_frame, width = 15, anchor = "w")
payout_ratio.grid(row = 2, column = 3)
ex_div_label = tkinter.Label(financial_frame, width = 15, anchor = "w", text = "Ex-Dividend Date:")
ex_div_label.grid(row = 2, column = 4)
ex_div = tkinter.Label(financial_frame, width = 15, anchor = "w")
ex_div.grid(row = 2, column = 5)
pe_fwd_label = tkinter.Label(financial_frame, anchor = "w", width = 15, text = "P/E Ratio (FWD):")
pe_fwd_label.grid(row = 3, column = 2)
pe_fwd = tkinter.Label(financial_frame, width = 15, anchor = "w")
pe_fwd.grid(row = 3, column = 3)
next_earn_lab = tkinter.Label(financial_frame, width = 15, anchor = "w", text = "Next Earnings (Est.):")
next_earn_lab.grid(row = 3, column = 4)
next_earn = tkinter.Label(financial_frame, width = 15, anchor = "w")
next_earn.grid(row = 3, column = 5)

# add ex date and pay date, free cash flow, fcf yield maybe (free cash flow / market cap), fcf payout ratio



gui.geometry("700x500")
gui.mainloop()
