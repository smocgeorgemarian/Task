from scrapper import Scrapper


def main():
    scrapper = Scrapper(URL="https://samples.vx-underground.org/samples/Families/",
                        api_URL="http://127.0.0.1:8000")
    scrapper.parse_data()
    scrapper.add_data_to_database()


if __name__ == '__main__':
    main()
