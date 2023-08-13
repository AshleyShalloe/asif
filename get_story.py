import json
import typing
import requests
from bs4 import BeautifulSoup as bs
from bs4 import Tag, NavigableString

def remove_double_newlines(input_text):
    while "\n\n" in input_text:
        input_text = input_text.replace("\n\n", "\n")
    return input_text


def get_text(tag: Tag) -> str:
    _inline_elements = {
        "a",
        "span",
        "em",
        "strong",
        "u",
        "i",
        "font",
        "mark",
        "label",
        "s",
        "sub",
        "sup",
        "tt",
        "bdo",
        "button",
        "cite",
        "del",
        "b",
        "a",
        "font",
    }

    def _get_text(tag: Tag) -> typing.Generator:
        for child in tag.children:
            if isinstance(child, Tag):
                # if the tag is a block type tag then yield new lines before after
                is_block_element = child.name not in _inline_elements
                if is_block_element:
                    yield "\n"
                yield from ["\n"] if child.name == "br" else _get_text(child)
                if is_block_element:
                    yield "\n"
            elif isinstance(child, NavigableString):
                yield child.string

    return remove_double_newlines("".join(_get_text(tag))).strip()


def retrieve_and_normalise_story(url):
    return_dict = {}
    soup = requests.get(url).text
    
    try:
        return_dict["story"] = "\n".join(
            [
                f"<p>{x}</p>"
                for x in get_text(
                    bs(soup, features="lxml").find("div", {"id": "maincontent"})
                ).split("\n")
            ]
        )
    except:
        return_dict["story"] = "<p>Oh well that's not very good is it. We've entirely failed to parse the story.</p>"
    
    try:
        return_dict["headline"] = "\n".join(
            [
                f"<p>{x}</p>"
                for x in get_text(
                    bs(soup, features="lxml").find("div", {"data-gu-name": "headline"})
                ).split("\n")
            ]
        )
    except:
        return_dict["headline"] = "Error parsing headline"
    
    try:
        return_dict["meta"] = "\n".join(
            [
                f"<p>{x}</p>"
                for x in get_text(
                    bs(soup, features="lxml").find("aside", {"data-gu-name": "meta"})
                ).split("\n")
            ]
        )
    except:
        return_dict["meta"] = "Error parsing meta"
    
    try:
        return_dict["standfirst"] = "\n".join(
            [
                f"<p>{x}</p>"
                for x in get_text(
                    bs(soup, features="lxml").find("div", {"data-gu-name": "standfirst"})
                ).split("\n")
            ]
        )
    except:
        return_dict["standfirst"] = "Error parsing whatever a standfirst is"
        
    try:
        return_dict["picture"] = bs(soup, features="lxml").find("div", {"data-gu-name": "media"}).find("img").get("src", "")
    except:
        return_dict["picture"] = ""
    
    return return_dict

def get_story_image_by_url(url):
    soup = requests.get(url).text
    
    try:
        return bs(soup, features="lxml").find("div", {"data-gu-name": "media"}).find("img").get("src", "")
    except:
        return None