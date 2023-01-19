import os
import time
import shutil
import json
# import toml
import jinja2
# import transit


def gen():
    if os.path.isdir("dist"):
        shutil.rmtree("dist")
    elif os.path.exists("dist"):
        os.remove("dist")
    os.mkdir("dist")
    with open("src/timetable.json") as f:
        tt = json.load(f)
    with open("src/index.html") as f:
        tpl = jinja2.Template(f.read())
    rendered = tpl.render(timetable=json.dumps(tt))
    with open("dist/index.html", "w") as f:
        f.write(rendered)
    with open("src/sw.js") as f:
        tpl = jinja2.Template(f.read())
    rendered = tpl.render(time=int(time.time()))
    with open("dist/sw.js", "w") as f:
        f.write(rendered)
    shutil.copy("src/manifest.json", "dist/manifest.json")
    # with open("dist/transit.json", "w") as f:
    #     json.dump(transit.main(), f)


if __name__ == "__main__":
    gen()
