"""
Sphinx/docutils extension to create links to pyDoctor documentation using a
RestructuredText interpreted text role that looks like this::

    :api:`python_object_to_link_to <label>`

for example::

    :api:`twisted.internet.defer.Deferred <Deferred>`

"""

from twisted.python.reflect import namedAny
from types import FunctionType


def make_api_link(name, rawtext, text, lineno, inliner,
                  options={}, content=[]):

    from docutils import nodes, utils

    # quick, dirty, and ugly...
    if '<' in text and '>' in text:
        full_name, label = text.split('<')
        full_name = full_name.strip()
        label = label.strip('>').strip()
    else:
        full_name = label = text

    #get the base url for api links from the config file
    env = inliner.document.settings.env
    if full_name.startswith("twisted"):
        base_url = env.config.apilinks_base_url
    else:
        base_url = "https://twisted.org/tubes/docs/"

    # not really sufficient, but just testing...
    # ...hmmm, maybe this is good enough after all
    try:
        consider = namedAny(full_name)
    except:
        consider = None
    if isinstance(consider, (type(None), FunctionType)):
        dot_path, fragment = full_name.rsplit(".", 1)
        if fragment:
            fragment = "#" + fragment
    else:
        dot_path = full_name
        fragment = ""
    ref = ''.join((base_url, dot_path, '.html', fragment))

    options.update(classes=["api"])

    node = nodes.reference(rawtext, utils.unescape(label), refuri=ref,
                           **options)

    nodes = [node]
    sys_msgs = []
    return nodes, sys_msgs


# setup function to register the extension

def setup(app):
    app.add_config_value('apilinks_base_url',
                         'https://twistedmatrix.com/documents/current/api/',
                         'env')
    app.add_role('api', make_api_link)
