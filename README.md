# asif - a syndicated information feed

## What is this?

At present, a convoluted, half-implemented RSS feed reader for a specific website that I don't much like.

I may finish this at some point.

## That sounds wonderful, how do I use it?

If you insist...

* Clone the repo and cd to the directory
* Run `start_flask.sh`
* Go to `127.0.0.1:5000` in your browser

You should now have something that looks almost entirely, but not completely, unlike a news app.

## That didn't work

Of course not, silly.

You probably need to install a bunch of dependencies like `BeautifulSoup`. `feedparser`, `pandas`, `requests`, `flask` and `flask-cors`.

You can probably do this by running:

```sh
pip install feedparser pandas requests beautifulsoup4 flask-cors
```

## That still didn't work

Oh well.

## No wait, it's working!

That's great! Glad you figured it out.