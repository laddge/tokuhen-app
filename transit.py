import datetime
import pytz
from bs4 import BeautifulSoup
import requests
from concurrent import futures


def get(date, direction):
    times = []
    res = []
    for _ in range(10):
        to = ["%E5%B1%8B%E4%BB%A3", "%E7%AF%A0%E3%83%8E%E4%BA%95"][direction]
        if times:
            date = times[-1] + datetime.timedelta(minutes=1)
        m1 = str(date.minute)[0] if date.minute > 9 else 0
        m2 = str(date.minute)[1] if date.minute > 9 else date.minute
        url = (
            "https://transit.yahoo.co.jp/search/print"
            + f"?from=%E5%B1%8B%E4%BB%A3%E9%AB%98%E6%A0%A1%E5%89%8D&to={to}"
            + f"&y={date.year}&m={date.month:02}&d={date.day:02}&hh={date.hour:02}"
            + f"&m1={m1}&m2={m2}"
        )
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        time = soup.select(".routeSummary .time span")[0].contents[0]
        if int(time.split(":")[0]) < date.hour:
            date += datetime.timedelta(days=1)
        times.append(
            date.replace(
                hour=int(time.split(":")[0]),
                minute=int(time.split(":")[1]),
                second=0,
                microsecond=0,
            )
        )
        dest = soup.select(".transport div")[0].contents[-1].split("・")[-1]
        res.append([times[-1].isoformat(), dest, url.replace("print", "result")])
    return res


def main():
    date = datetime.datetime.now(pytz.timezone("Asia/Tokyo"))
    rets = []
    with futures.ThreadPoolExecutor() as executor:
        for i in range(2):
            rets.append(executor.submit(get, date, i))
    rets = [x.result() for x in rets]
    return {
        "date": date.isoformat(),
        "ueda": rets[0],
        "nagano": rets[1],
    }


if __name__ == "__main__":
    print(main())
