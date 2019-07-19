#!/usr/bin/env python3

from socktun import Proxy

if __name__ == '__main__':
    try:
        st = Proxy()
        st.start()
    except KeyboardInterrupt:
        exit(0)
