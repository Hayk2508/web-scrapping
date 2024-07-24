import requests
import threading


def send_request():
    print("Started")
    requests.get(
        "http://localhost:8000/api/parsers/parse/?url=https://preply.com/en/tutor-signup&parse_type=images"
    )
    print("Processed")


if __name__ == "__main__":
    threads = [threading.Thread(target=send_request) for i in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
