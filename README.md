# WitchHunters
Keyword searching browser that saves multiple web pages into links, images and documents to be preserved as an evidence of disinformation

### Requirements
  - [Python 3](https://www.python.org)
  - [Google Chrome](https://www.google.co.kr/chrome/browser/desktop/) (Or you can use other browsers supported by [Selenium](http://www.seleniumhq.org/))
  - [Chrome driver](https://sites.google.com/a/chromium.org/chromedriver/home)
  - [Selenium](http://www.seleniumhq.org/) for browser automation
  - [Pillow](https://python-pillow.org/) for image processing
  - [lxml](http://lxml.de/) for xpath search

> `cinst python3 googlechrome -y` with administrator privilege and [Chocolatey](https://chocolatey.org/) installed.
> `pip install selenium Pillow` with administrator privilege.
> `pip install lxml-3.6.0-cp35-cp35m-win_amd64.whl` with wheel file from [lxml](http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml) (Windows only)

### Supported sites (Ask me if you want any other)
  - http://blog.naver.com
  - http://cafe.naver.com

### Usage
  - You do the search with other browser and preserve target webpages with this program by giving the URL.
    `python capture.py` for continuous input
    `python capture.py [URL]` for single capture
  - Automatically search supported sites with a keyword and preserve all available pages.
    `python main.py` for continuous keyword input
    `python main.py [Keyword]` for single keyword
  - After capture utilities are accessible by `python util.py`
  - Press Ctrl+C to quit from continuous input

### Related application
  - [SplitPrint](http://openwrld.egloos.com/2827456) : When you need to print the captured long images as separated paper pages to hand it over.
