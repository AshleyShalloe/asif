## asif - a syndicated information feed

import feedparser
import pandas as pd

guardian_url = "https://www.theguardian.com/uk/rss"

def get_database_fields(feed_url):
    """
    Takes in a feed URL, returns a dataframe with
    the fields defined below
    """
    parsed_feed = feedparser.parse(feed_url)

    return_list = []

    for i in range(0, len(parsed_feed["entries"])):
        title     = parsed_feed["entries"][i].get("title", parsed_feed.get("feed", {}).get("title", "no title"))
        url       = parsed_feed["entries"][i].get("links", {"href": feed_url})[0]["href"]
        summary   = parsed_feed["entries"][i].get("summary", "no summary")
        media_url = parsed_feed["entries"][i].get("media_content", [{}])[0].get("url")
        author    = parsed_feed["entries"][i].get("author", parsed_feed.get("feed", {}).get("title", "no author"))
        updated   = parsed_feed["entries"][i].get("updated", None)
        category  = parsed_feed["entries"][i].get("tags", [{}])[0].get("term", [])
        return_list.append([title, url, summary, media_url, author, updated, category])

    return_df = pd.DataFrame(return_list).rename({
                                                    0: "title",
                                                    1: "story_url",
                                                    2: "summary",
                                                    3: "media_url",
                                                    4: "author",
                                                    5: "updated",
                                                    6: "category"
                                                }, axis=1)
    
    return_df["updated"] = pd.to_datetime(return_df["updated"], utc=True)

    return return_df

def retrieve_and_write_updated_json():
    ## somewhere here you should check the etags
    ## to save updating if there is no need
    meta_df = get_database_fields(guardian_url)

    with open("static/asif.json", "w") as outfile:
        outfile.write(meta_df.to_json(orient="records"))