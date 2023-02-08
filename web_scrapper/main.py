from scrapper import Scrapper


def main():
    scrapper = Scrapper("https://samples.vx-underground.org/samples/Families/")
    scrapper.parse_data()
    scrapper.pretty_print_data()


if __name__ == '__main__':
    main()
