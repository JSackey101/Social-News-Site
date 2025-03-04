# Social News Site

## Description

Contains both the Backend and the Frontend for a Social News Site capable of:

- Displaying news articles (with links to their source) with scores.
- Allowing users to upvote and downvote the news articles.
- Allowing users to add articles to the page with a link and a title.
- Allowing users to delete and edit articles.
- Allowing users to scrape articles from another news site. (only works for the BBC.)

## Installation Instructions

Install dependencies with:

```
pip install -r requirements.txt

```
## Before Use

Change the port from 8000 (Default) to whatever works for your device.

## Endpoints

### / - Methods: GET

Default endpoint. Returns the base HTML for the site.

### /add - Methods: GET

#### Methods

- GET

Returns the HTML for adding an article to the site.

### /stories - Methods: GET, POST, Queries: search, sort, order

#### Methods

- GET

Returns article data depending on the queries given.

- POST

Adds a new article to the list. 

Request Body:

- 'url' header - containing a link to the source of the article.
- 'title' header - containing the title of the news article.

#### Queries

- search

Filters the articles returned based on whether given parameter is found in the title. Not case-sensitive. 

- sort

Sorts stories based on given parameter.

Accepted Parameters:

- 'title' - Alphabetic order of title.
- 'score' - Ordered by score.
- 'created' - Ordered by creation date.
- 'modified' - Ordered by modification date. (including up and downvotes)

- order

Orders stories in the given way. Default is 'ascending'.

Accepted Parameters:

- 'ascending' - Order is lowest to highest.
- 'descending' - Order is highest to lowest

### /stories/<id>/votes - Methods: POST

#### Parameters

- id - ID of the article that is to be updated. ID must be a whole number.

#### Methods

- POST

Updates the score of an article in the list. Updates the modification date of that article to the current time.

Request Body:

- 'direction' header - should contain either 'up' representing a score increase of 1 or 'down' representing a score decrease of 1.

Notes:

Score cannot decrease below 0. Trying to send a 'down' request to an article with a score of 0 will result in an error.

### /stories/<id> - Methods: PATCH, DELETE

#### Parameters

- id - ID of the article that is to be updated. ID must be a whole number.

#### Methods

- PATCH

Updates the URL/website and/or title of an article in the list. Updates the modification date of that article to the current time.

Request Body:

- 'url' header - containing a link to the source of the article.
- 'title' header - containing the title of the news article.

Notes:

- Request body can contain either a url or title or both. Must have at least one of the two. 

- DELETE

Deletes an article in the list.

### /scrape - Methods: GET, POST

#### Methods

- GET

Returns the HTML for accepting a link to scrape news articles from.

- POST

Takes news articles from a given link and adds them to the article list.

Request Body:

- 'url' header - containing a link to a site with articles to scrape and add to the site.

Notes: 

- URL must be a valid URL starting with http:// or https://

- Scraping currently only works for the [BBC](https://www.bbc.co.uk) site. 

## Future Work

- Expanding scraping to work for more news sites.

- Moving website storage to a PostgreSQL database rather than a CSV.
