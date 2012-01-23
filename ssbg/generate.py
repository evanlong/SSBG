#!/usr/bin/env python

import sys
import os
import datetime
import shutil
import codecs
from jinja2 import Environment, FileSystemLoader, Template
import markdown
import PyRSS2Gen
import settings

#blogger data import
#analytics

def _markdownRender(renderedContent, **kwargs):
    template = Template(renderedContent)
    return template.render(**kwargs)

def _renderTemplateToFile(template, outputPath, **kwargs):
    kwargs["static_path"] = os.path.join(kwargs.get("offset_prefix", ""), "static")
    kwargs["image_path"] = os.path.join(kwargs["static_path"], "img/")
    kwargs["rootUrl"] = settings.BLOG_URL
    result = template.render(**kwargs)
    result = _markdownRender(result, **kwargs)
    with codecs.open(outputPath, "w", encoding="utf-8") as f:
        f.write(result)

def _renderTemplateForRoot(template, outputPath, **kwargs):
    kwargs["offset_prefix"] = ""
    _renderTemplateToFile(template, outputPath, **kwargs)

def _renderTemplateForSubdir(template, outputPath, **kwargs):
    kwargs["offset_prefix"] = "../"
    _renderTemplateToFile(template, outputPath, **kwargs)

def _outputDirPathFor(subdir):
    outputDirectory = os.path.join(settings.OUTPUT_DIR, subdir)
    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)

    return outputDirectory

def _renderRssFeedToFile(postMetaData, outfile):
    items = []
    for p in postMetaData:
        url = os.path.join(settings.BLOG_URL, p["remoteUrl"])
        items.append(PyRSS2Gen.RSSItem(
                title = p["title"],
                link = url,
                pubDate = p["date"],
                description = p["content"],
                guid = PyRSS2Gen.Guid(url)
                ))

    rss = PyRSS2Gen.RSS2(
        title = "infectmac.com",
        link = settings.BLOG_URL,
        description = "a blog of fun",
        lastBuildDate = datetime.datetime.utcnow(),
        items = items
        )

    with open(outfile, "w") as f:
        rss.write_xml(f, encoding="utf-8")

def _formatDate(date, fmt="%B %d, %Y"):
    return date.strftime(fmt)

def _boolToVisibility(value):
    return "visible;" if value else "hidden;"

_env = Environment(loader=FileSystemLoader("templates"), autoescape=False)
_env.filters["formatdate"] = _formatDate
_env.filters["boolToVisibility"] = _boolToVisibility

def _generatePosts():
    ### begin constants
    OUTPUT_POST_DIR = _outputDirPathFor("posts")
    OUTPUT_PAGE_DIR = _outputDirPathFor("pages")
    OUTPUT_INDEX_HTML = os.path.join(settings.OUTPUT_DIR, "index.html")
    OUTPUT_ABOUT_HTML = os.path.join(settings.OUTPUT_DIR, "about.html")
    OUTPUT_POSTS_HTML = os.path.join(settings.OUTPUT_DIR, "posts.html")
    OUTPUT_RSS_XML = os.path.join(settings.OUTPUT_DIR, "rss.xml")

    indexTemplate = _env.get_template("index.html")
    postsTemplate = _env.get_template("posts.html")
    aboutTemplate = _env.get_template("about.html")
    ### end constants

    ### begin helper funcs
    def _pagePath(number):
        return os.path.join("pages", "%d.html" % number)

    def _pathForOutput(path):
        return os.path.join(settings.OUTPUT_DIR, path)
    ### end helper funcs

    postMetaData = []
    for f in os.listdir("posts"):
        fParts = f.split("-")
        date = datetime.datetime(*[int(i) for i in fParts[:5]])
        title = ' '.join(fParts[5:])
        title = title[:title.rindex(os.extsep)]
        with codecs.open(os.path.join("posts", f), "r", encoding="utf-8") as postFile:
            fileContents = postFile.read()
            p = {
                "title": title,
                "date": date,
                "content": markdown.markdown(fileContents, ["codehilite"]),
                "remoteUrl": os.path.join("posts", "%s.html" % (f[:f.rindex(os.extsep)]))
                }
            postMetaData.append(p)

    postMetaData.sort(key=lambda p: p["date"], reverse=True)

    pagesMetaData = []
    pageCount = 0
    postIdx = 0
    for postIdx,post in zip(range(len(postMetaData)), postMetaData):
        pagesMetaData.append(post)

        postIsLast = (post == postMetaData[-1])
        postIsFirst = (post == postMetaData[0])
        
        _renderTemplateForSubdir(indexTemplate,
                                 _pathForOutput(post["remoteUrl"]),
                                 posts=[post],
                                 newerPath = "" if postIsFirst else postMetaData[postIdx-1]["remoteUrl"],
                                 olderPath = "" if postIsLast else postMetaData[postIdx+1]["remoteUrl"])

        if len(pagesMetaData) == settings.POSTS_PER_PAGE or postIsLast:
            _renderTemplateForSubdir(indexTemplate,
                                     _pathForOutput(_pagePath(pageCount)),
                                     posts=pagesMetaData,
                                     newerPath = "" if pageCount == 0 else _pagePath(pageCount - 1),
                                     olderPath = "" if postIsLast else _pagePath(pageCount + 1))

            #special case the index
            if pageCount == 0:
                _renderTemplateForRoot(indexTemplate,
                                       OUTPUT_INDEX_HTML,
                                       posts = pagesMetaData,
                                       olderPath = "" if postIsLast else _pagePath(1))

            pagesMetaData = []
            pageCount += 1

    # list of all the blog posts
    _renderTemplateForRoot(postsTemplate, OUTPUT_POSTS_HTML, pairs=postMetaData)

    #about page
    with codecs.open("about.markdown", "r", encoding="utf-8") as aboutFile:
        _renderTemplateForRoot(aboutTemplate, OUTPUT_ABOUT_HTML, content=markdown.markdown(aboutFile.read()))

    #rss feed
    _renderRssFeedToFile(postMetaData, OUTPUT_RSS_XML)

def main():
    assert len(sys.argv) >= 2

    subcommand = sys.argv[1]
    if subcommand == "new_post":
        assert len(sys.argv) >= 3
        title = sys.argv[2]
        fname = "%s-%s.markdown" % (datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"), title.replace(" ", "-"))
        filePath = os.path.join("posts", fname)
        with open(filePath, "w") as f: pass
    elif subcommand == "make":
        shutil.rmtree(settings.OUTPUT_DIR, ignore_errors=True)
        os.mkdir(settings.OUTPUT_DIR)
        shutil.copytree("static", os.path.join(settings.OUTPUT_DIR, "static"))
        _generatePosts()

if __name__ == "__main__":
    main()

