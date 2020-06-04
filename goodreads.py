import requests

# Getting Goodreads APIs


def main():
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "FIbCP1B0yajXYRYbsLujng", "isbns": "9781632168146"})
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")
    data = res.json()
    print(data)


if __name__ == "__main__":
    main()
