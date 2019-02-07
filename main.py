import requests
import os
import datetime
import csv

# Credentials, please set to correct username and password
credentials = 'username', 'password'
# Your Zendesk URL
zendesk = 'https://[your-url].zendesk.com'
language = 'ja'

# Makes backup path
date = datetime.date.today()
backup_path = os.path.join(str(date), language)
if not os.path.exists(backup_path):
    os.makedirs(backup_path)

# For CSV logging
log = []

# API Endpoint Lists
articles = zendesk + '/api/v2/help_center/{locale}/articles.json'.format(locale=language.lower())
sections = zendesk + '/api/v2/help_center/{locale}/sections.json'.format(locale=language.lower())
categories = zendesk + '/api/v2/help_center/{locale}/categories.json'.format(locale=language.lower())

# First retrive the sections and categories JSON data
response = requests.get(sections, auth=credentials)
if response.status_code != 200:
    print('Failed to retrieve sections with error {}'.format(response.status_code))
    exit()

sections = response.json()

response = requests.get(categories, auth=credentials)
if response.status_code != 200:
    print('Failed to retrieve categories with error {}'.format(response.status_code))
    exit()

categories = response.json()

# Begin the article process
while articles:
    response = requests.get(articles, auth=credentials)
    if response.status_code != 200:
        print('Failed to retrieve articles with error {}'.format(response.status_code))
        exit()

    data = response.json()

    for article in data['articles']:
        if article['body'] is None:
            continue

        # # Reserved for HTML processing
        # title = '<h1>' + article['title'] + '</h1>'
        # filename = '{id}.html'.format(id=article['id'])
        # with open(os.path.join(backup_path, filename), mode='w', encoding='utf-8') as f:
        #     f.write(title + '\n' + article['body'])

        for section in sections['sections']:
            if section['id'] == article['section_id']:
                sectionsname = section['name']
                categoriesid = section['category_id']

        for category in categories['categories']:
            if category['id'] == categoriesid:
                categoriesname = category['name']

        print('{id} copied!'.format(id=article['id']))
        log.append((categoriesname, sectionsname, article['title'], article['body']))

    articles = data['next_page']

# Write to CSV
filename = 'zendesk.csv'

with open(os.path.join(backup_path, filename), mode='w', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow( ('Category', 'Section', 'Title', 'Body') )
    for article in log:
        writer.writerow(article)
