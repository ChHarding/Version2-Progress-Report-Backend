import os
os.chdir('templates')

from bs4 import BeautifulSoup

# Open the file in read mode
with open('index.html.orig', 'r') as file:
    soup = BeautifulSoup(file.read(), 'html.parser')

# Update img src
for img in soup.find_all('img', src=True):
    if img['src'].startswith('images/'):
        img['src'] = '/static/' + img['src']

# Update link href (CSS)
for link in soup.find_all('link', href=True):
    if link['href'].startswith('css/'):
        link['href'] = '/static/' + link['href']

# Update script src (JS)
for script in soup.find_all('script', src=True):
    if script['src'].startswith('js/'):
        script['src'] = '/static/' + script['src']

# Write the file out again
with open('index.html', 'w') as file:
    file.write(str(soup))