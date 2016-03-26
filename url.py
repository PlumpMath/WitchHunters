from main import *

def capture_url(url):
  if not url.startswith('http://') or not url.startswith('https://'):
    url = 'http://' + url
  chrome.get(url) # target page
  sleep(1) # or implicit/explicit wait for AJAX be done
  fname = url[7:].replace('/','-').replace('?', '-')
  screenshot(fname)
  source(fname)
  urllink(fname, url)


if __name__ == '__main__':
  from sys import argv
  while True:
    capture_url(input('URL>') if len(argv) == 1 else argv[1])
    if len(argv) > 1:
      break
  chrome.close()
