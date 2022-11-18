import os
import shutil
import json
import toml


def gen():
    if os.path.isdir("dist"):
        shutil.rmtree("dist")
    elif os.path.exists("dist"):
        os.remove("dist")
    os.mkdir("dist")
    with open("timetable.toml") as f:
        tt = toml.load(f)
    with open("dist/timetable.json", "w") as f:
        json.dump(tt, f)


if __name__ == "__main__":
    gen()
