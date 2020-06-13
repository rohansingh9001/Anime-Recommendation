from stem.control import Controller
from stem import Signal
import time

def main():
    while True:
        time.sleep(10)
        print("Rotating IP")
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password="Tarun@2001")
            controller.signal(Signal.NEWNYM)

if __name__=="__main__":
    main()



