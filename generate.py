import os
import shutil
import json
import toml
import jinja2
# import transit


def gen():
    if os.path.isdir("dist"):
        shutil.rmtree("dist")
    elif os.path.exists("dist"):
        os.remove("dist")
    os.mkdir("dist")
    with open("src/timetable.toml") as f:
        tt = toml.load(f)
    with open("dist/timetable.json", "w") as f:
        json.dump(tt, f)
    with open("src/index.html") as f:
        tpl = jinja2.Template(f.read())
    rendered = tpl.render(courses=tt["courses"])
    with open("dist/index.html", "w") as f:
        f.write(rendered)
    # with open("dist/transit.json", "w") as f:
    #     json.dump(transit.main(), f)


if __name__ == "__main__":
    gen()
