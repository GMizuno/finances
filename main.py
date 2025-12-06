import pendulum
import os


def main() -> str:
    print(pendulum.today())

    print(os.listdir())

    return ""

if __name__ == '__main__':
    main()
