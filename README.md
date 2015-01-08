<h1>NewsSummarizer</h1>
==============

NewsSummarizer is a Python web application that summarizes the text content of a webpage.

<h2>How It Works</h2>

<ul>
<li>NewsSummarizer prompts the user for a URL and it saves the webpage as an html file using urllib.request library</li>
<li>Next we use the BeautifulSoup library to remove all the CSS and JavaScript code from the html file and we store the text and its title</li>
<li>We use the Gensim NLP library and run a similarity query on the text using the title as the query</li>
<li>We return a concise 5 sentence summary of the webpage</li>

</ul>

Sample Output:
Here's a BBC Article about the declining price of oil:
<img scr = "http://imgur.com/FZHBZXd">

Here's a QuickNews summary:
<img scr = "http://imgur.com/CJmfmXv">

