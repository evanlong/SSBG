## SSBG (Simple Static Blog Generator)

This is my simple static blog generator used for <http://www.infectmac.com/>. It
is meant for me. But maybe someone else will find it of some use.

### Features:

* Write posts in mardown and have code highlighted with pygments
* Generates individual posts as well as pages of posts
* RSS feed generation

### File and Directory Layout:

* `generate.py` - Program used to generate the blog
* `settings.py` - configuration for `generate.py`
* `about.markdown` - File that will be rendered to `{output}/about.html`
* `static/` - js, css, and images used for the blog
* `templates/` - Templates used for the different pages
   * `base.html` - Root template from which all others derive
   * `about.html` - Template for rendered contents of `about.markdown`
   * `index.html` - Individual post or a list of posts. Results in files
   rendered to `{output}/index.html`, each `{output}/pages/{n}.html`, and each
   `/posts/YEAR-MONTH-DAY-HOUR-MINUTE-Title-Here.html`
   * `posts.html` - List of all the posts the blog contains

### Settings

The settings are specified with global variables in `settings.py`.

* `BLOG_URL` - url to the root of the blog. Example: `http://infectmac.com/`
* `OUTPUT_DIR` - the directory that the blog will be emitted to
* `POSTS_PER_PAGE` - Maximum number of posts that should be show on a single
page
* `DEPLOY_CMD` - The shell command that will be run from the `OUTPUT_DIR` in
  order to deploy the latest build. For example this could be:
  `git add .; git commit -am "new post"; git push`
* `TEST_OUTPUT_DIR` - When the `test` subcommand is used the `OUTPUT_DIR` and
  `DEPLOY_CMD` are ignored. Instead the output is redirected to
  `TEST_OUTPUT_DIR`

### Usage:

`generate.py` has the following subcommands:

* `make` - Generate the blog and output it to the directory specified in
`settings.py`.
* `new_post` - Accepts a single argument for the title of the post. It will then
create a file with the format `YEAR-MONTH-DAY-HOUR-MINUTE-Title-Here.markdown`
in the `posts`.
* `test` - The same as make but does not run the deploy command

### Markdown extras

The markdown files have extra variables that can be useful when linking to blog
content. They are
* `{{image_path}}` - relative path to `static/img/`
* `{{posts_path}}` - relative path to `posts/`
* `{{static_path}}` - relative path to `static/`

Example usage might be: `![alt text]({{image_path}}woman.jpg)` or
`[link for file download]({{static_path}}files/download.zip)`

Both variables will render as relative paths to either the image or static
directory.

### Tips

This is a quick and dirty way to link to images:
`[![procmon]({{image_path}}procmon.png)]({{image_path}}procmon.png)`

### Credits:

* [Pygments](http://pygments.org/)
* [Jinja2](http://jinja.pocoo.org/docs/)
* [Markdown in Python](http://www.freewisdom.org/projects/python-markdown/)
* [PyRSS2Gen](http://www.dalkescientific.com/Python/PyRSS2Gen.html)
* [1140 CSS Grid](http://cssgrid.net/)

