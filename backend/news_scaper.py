def get_html(url):
  page = urlopen(url)
  html_bytes = page.read()
  html = html_bytes.decode('utf_8')
  return html_doc

if __name__ == "__main__":
	bbc_url = "http://bbc.co.uk"
	bbc_html_doc = get_html(bbc_url)
