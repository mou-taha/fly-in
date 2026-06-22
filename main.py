from helper.parser.dataParser import DataParser


def main():
    print("Hello from fly-in!")
    data_parser = DataParser()
    print(data_parser.parseData("./data"))


if __name__ == "__main__":
    main()
