# coding=utf-8
from lxml import html

import re
from time import sleep

from urllib.request import urlopen
from urllib.parse import urlencode

from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By

wd = webdriver.Chrome() # can be Edge, FireFox, etc...
wd.maximize_window()
wd.implicitly_wait(10)

def urllink(fname, url):
  fname += '.url'
  with open(fname, 'w') as f:
    f.write('[{000214A0-0000-0000-C000-000000000046}]\n\
Prop3=19,2\n\
[InternetShortcut]\n\
IDList=\n\
URL=' + url + '\n\
IconIndex=13\n\
HotKey=0\n\
IconFile=%WINDIR%\system32\SHELL32.dll')
  print('saved to', fname)

def source(fname, frame=''):
  global wd
  fname += '.htm'
  if frame:
    wd.switch_to.frame(frame)
  with open(fname, 'w', encoding='utf-8') as f:
    f.write(wd.page_source)
  if frame:
    wd.switch_to.default_content()
  print('saved to', fname)

from sys import platform
FONT_PATH = '%windir%\\fonts\\segoeui.ttf' if platform == 'win32' else '/usr/share/fonts/ttf-ancient-scripts/Aegean600.ttf'

def screenshot(fname, frame='', url=''):
  from PIL import Image, ImageFile, ImageDraw, ImageFont
  global wd
  fname += '.png'
  wh=wd.execute_script('return window.innerHeight')
  ww=wd.execute_script('return window.innerWidth')
  th=wd.execute_script('return %s.body.parentNode.scrollHeight'%(frame if frame else 'document',))
  #tw=wd.execute_script('return %s.body.parentNode.scrollWidth'%frame)
  font = ImageFont.truetype(FONT_PATH, 12)
  mgn = 30 if url else 15
  img=Image.new('RGB', (ww, th+mgn))
  d = ImageDraw.Draw(img)
  d.text((3, 3), 'Image taken with WitchHunters http://github.com/chidea/WitchHunters', fill=(255,255,255), font=font)
  if url:
    d.text((3, 15), 'From : ' + url, fill=(255,255,255), font=font)
  for sh in range(0, th, wh):
    wd.execute_script('%s.scroll(0,%d)'%(frame if frame else 'window', sh))
    sleep(.1)
    p=ImageFile.Parser()
    p.feed(wd.get_screenshot_as_png())
    t=p.close()
    if th-sh<wh: # end of screenshot is smaller than screen
      t=t.crop((0,wh-(th-sh),ww,wh))
      img.paste(t, (0,mgn+sh,ww,mgn+th))
    else:
      img.paste(t, (0,mgn+sh,ww,mgn+sh+wh))
    t.close()
  img.save(fname)
  print('saved to', fname)

pat1 = re.compile(r'http://cafe.naver.com/(.+)/(.+)')
def parse_naver_cafe(r):
  global wd
  l = r.xpath('//*[@id="ArticleSearchResultArea"]/li/dl')
  l.reverse()
  for dl in l:
    link = dl.xpath('dt/a')[0]
    title = link.text_content()
    link = link.attrib['href']
    content_sum = dl.xpath('dd[1]')[0]
    date = content_sum.text.strip()
    content_sum = content_sum.xpath('dd')[0].text_content()
    fname = date[:-1] + '-' + '-'.join(pat1.match(link).groups())
    try:
      print(date, link, title, content_sum)
    except UnicodeEncodeError:
      pass
    wd.get(link)
    wd.find_element_by_id('denyNamelessLayer')
    #wd.switch_to.frame(wd.find_element_by_id('cafe_main'))
    #try:
    #  wd.implicitly_wait(1)
    #  wd.find_element_by_id('basisElement')
    #  wd.switch_to.default_content()
    if len(wd.window_handles) > 1 :
      wd.switch_to.window(wd.window_handles[-1])
      wd.close()
      wd.switch_to.window(wd.window_handles[0])
    else:
      screenshot(fname, url=link)
      source(fname, 'cafe_main')
      urllink(link)
    #except selenium.common.exceptions.NoSuchElementException:
    #  pass

  #'//*[@id="ArticleSearchResultArea"]/li[1]/dl/dd[2]'
  #for l in links:
  #  print(l)

pat2=re.compile(r'http://blog.naver.com/([^?]+)\?Redirect=Log&logNo=([^&]+)&from=section')
def parse_naver_blog(r):
  global wd
  l = r.xpath('//*[@id="blogSearchForm"]/div[2]/ul[3]/li')
  l.reverse()
  for dl in l:
    link = dl.xpath('h5/a')[0]
    title = link.text_content()
    link = link.attrib['href']
    content_sum = dl.xpath('div[2]/div/a')[0].text_content()
    date = dl.xpath('div[1]/span[2]')[0].text[:10]
    fname = date + '-'
    try:
      fname += '-'.join(pat2.match(link).groups())
    except:
      fname += link[7:].replace('/','-').replace('?', '-')
    try:
      print(date, link, title, content_sum)
    except UnicodeEncodeError:
      pass
    wd.get(link)
    mainframe='mainFrame'
    try:
      wd.find_element_by_id('hiddenFrame')
    except:pass
    try:
      wd.switch_to.frame('mainFrame')
    except:
      mainframe='screenFrame'
      wd.switch_to.frame(mainframe)
      wd.switch_to.frame('mainFrame')
    try:
      # open reply box
      wd.find_element(By.XPATH, '//*[@id="printPost1"]/tbody/tr/td[2]/div[contains(@class, "post-btn")]/div[3]/strong[1]/a').click()
    except: pass
    wd.switch_to.default_content()
    if mainframe != 'mainFrame':
      wd.switch_to.frame(mainframe)
    screenshot(fname, 'mainFrame', url=link)
    source(fname, 'mainFrame')
    urllink(fname, link)

from math import ceil
def find_last_cafe_page(h):
  try:
    cnt=int(r.xpath('//*[@id="SearchTotalCount"]')[0].text)
    return ceil(cnt/10) if cnt < 1000 else 100
  except: pass
  return 100

def find_last_blog_page(h):
  try:
    cnt=int(r.xpath('//*[@id="blogSearchForm"]/div[2]/p/em')[0].text[:-1])
    return ceil(cnt/10) if cnt < 4000 else 400 # max page
  except: pass
  return 400 

sites = {
    'http://section.cafe.naver.com/ArticleSearch.nhn':{
        'parse':parse_naver_cafe,
        'data':{
            'sortBy':1, # 0 for accuracy, 1 for latest
            'searchBy':0, # 0 for all, 1 for title only
            'duplicate':'false',
            #'period':'20150928'
          },
        'q':'query',
        'page':'page',
        'lastpage': find_last_cafe_page,
        'firstpage':1
      },
    'http://section.blog.naver.com/sub/SearchBlog.nhn':{
        'parse':parse_naver_blog,
        'data':{
            'type':'post',
            'option.orderBy':'date',
            #'term':'week', # comment out to search all, 'week', 'month' # 'period' to use startDate, endDate
            #'option.startDate':'2015-01-01',
            #'option.endDate':'2016-01-01'
          },
        'q':'option.keyword',
        'page':'option.page.currentPage',
        'lastpage': find_last_blog_page,
        'firstpage':1
      }
  }

if __name__ == '__main__':
  kwd = input('Keyword>')
  for s in sites:
    d=sites[s]['data']
    d[sites[s]['q']] = kwd
    d[sites[s]['page']] = sites[s]['firstpage']
    for i in range(sites[s]['lastpage'](html.fromstring(urlopen(s +'?'+ urlencode(d)).read().decode())), sites[s]['firstpage']-1, -1):
      d[sites[s]['page']] = i
      sites[s]['parse'](html.fromstring(urlopen(s +'?'+ urlencode(d)).read().decode()))

def test():
  s=list(sites.keys())[0]
  d=sites[s]['data']
  d[sites[s]['q']] = 'test'
  d[sites[s]['page']] = sites[s]['firstpage']
  r = html.fromstring(urlopen(s +'?'+ urlencode(d)).read().decode())
