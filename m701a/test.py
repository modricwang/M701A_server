from m701a.io_utils import connect_helper
import datetime
import time

def main():
    conn = connect_helper()
    while True:
        info = conn.read()
        print(datetime.datetime.now(), info)
        time.sleep(5)


if __name__ == '__main__':
    main()
