from authentek.internal import app
@app.route("/links")
def all_links():
    from flask import url_for
    links = []
    for rule in app.url_map.iter_rules():
        if len(rule.defaults) >= len(rule.arguments):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))

    return links
