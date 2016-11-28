# coding=utf-8

# Post-capture utilities that you may need.

from main import *

from os import listdir
from os.path import join
from os.path import isfile
from PIL import Image

def continuous_input_blog():
  global chrome
  try:
    while True:
      fname = input()
      url = fname[11:].split('-')
      if len(url) > 2 :
          url = ['-'.join(url[:-1]), url[-1]]
      if url[0].find('.') == -1:
        url ='http://blog.naver.com/' + url[0] + '\?Redirect=Log&logNo=' + url[1] + '&from=section'
      else:
        url = 'http://' + url[0] + '/' + url[1]
      print(fname, url)
      chrome.get(url)
      sleep(1)
      mainframe='mainFrame'
      try:
        chrome.switch_to.frame('mainFrame')
      except:
        mainframe='screenFrame'
        chrome.switch_to.frame(mainframe)
        chrome.switch_to.frame('mainFrame')
      try:
        # open reply box
        chrome.find_element(By.XPATH, '//*[@id="printPost1"]/tbody/tr/td[2]/div[contains(@class, "post-btn")]/div[3]/strong[1]/a').click()
      except: pass
      sleep(.2)
      chrome.switch_to.default_content()
      if mainframe != 'mainFrame':
        chrome.switch_to.frame(mainframe)
      screenshot(fname + '.png', 'mainFrame')
  except (EOFError, KeyboardInterrupt):
    pass

def continuous_input_cafe():
  try:
    while True:
      fname = input()
      url = fname[11:].split('-')
      url = 'http://cafe.naver.com/' + url[0] + '/' + url[1]
      chrome.get(url)
      chrome.find_element_by_id('denyNamelessLayer')
      screenshot(fname + '.png')
  except (EOFError, KeyboardInterrupt):
    pass

def retake_long_pictures_blog(trg=None):
  for f in listdir(trg):
    if not f.endswith('.png'): continue
    #if f.find('-blog.me-') == 10:
    #  nf = f[:-4].split('-')
    #  nf = '-'.join([nf[0], nf[2] + '.' + nf[1], nf[3]]) + f[-4:]
    #  rename(join('blog.naver.com', f), join('blog.naver.com', nf))
    if Image.open(join('blog.naver.com',f)).size[1] > 1000:
      url = f[11:-4].split('-')
      if len(url) > 2 :
          url = ['-'.join(url[:-1]), url[-1]]
      if url[0].find('.') == -1:
        url ='http://blog.naver.com/' + url[0] + '\?Redirect=Log&logNo=' + url[1] + '&from=section'
      else:
        url = 'http://' + url[0] + '/' + url[1]
      print(f, url)
      chrome.get(url)
      sleep(1)
      mainframe='mainFrame'
      try:
        chrome.switch_to.frame('mainFrame')
      except:
        mainframe='screenFrame'
        chrome.switch_to.frame(mainframe)
        chrome.switch_to.frame('mainFrame')
      try:
        # open reply box
        chrome.find_element(By.XPATH, '//*[@id="printPost1"]/tbody/tr/td[2]/div[contains(@class, "post-btn")]/div[3]/strong[1]/a').click()
      except: pass
      chrome.switch_to.default_content()
      if mainframe != 'mainFrame':
        chrome.switch_to.frame(mainframe)
      screenshot(f, 'mainFrame')

def retake_long_pictures_cafe(trg=None):
  for f in listdir(trg):
    if not f.endswith('.png'): continue
    if Image.open(join('cafe.naver.com',f)).size[1] > 1000:
      url = f[11:-4].split('-')
      url = 'http://cafe.naver.com/' + url[0] + '/' + url[1]
      chrome.get(url)
      screenshot(f)

def quit():
  global chrome
  chrome.close()
  exit()
if __name__ == '__main__':
  #for f in listdir('blog.naver.com/done'):
  #  if not f.endswith('.png'): continue
  #  if Image.open(join('blog.naver.com/done',f)).size[1] <= 2000:
  #    print(f)
  #exit()
  fns = (quit, continuous_input_blog, continuous_input_cafe, retake_long_pictures_blog, retake_long_pictures_cafe)
  while True:
    print('Select utility:\n\
0.Exit\n\
1.Continuous filename input(date.user.id) for blog.naver.com (quit with ctrl+c)\n\
2.Continuous filename input(date.user.id) for cafe.naver.com (quit with ctrl+c)\n\
3.Retake screenshots of long pictures(>1000px height)(blog.naver.com)\n\
4.Retake screenshots of long pictures(>1000px height)(cafe.naver.com)')
    i = input('>')
    if not i.isdigit() or int(i)>=len(fns): continue
    fns[int(i)]()

