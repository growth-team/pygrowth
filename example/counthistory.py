import pygrowth.counthistory
import pygrowth.eventfile
import os

example_dir = os.path.dirname(__file__)
example_fits_file_path = os.path.join(example_dir, "..", "tests/common/test_data/20180101_002728.fits.gz")


def extract_then_save_to_file():
    eventfile = pygrowth.eventfile.open(example_fits_file_path)

    counthistory_extractor = pygrowth.counthistory.CountHistoryExtractor()

    time_bin_sec = 15

    counthistory = counthistory_extractor.extract(eventfile, time_bin_sec)
    print(counthistory)

    # Write to file
    counthistory.write("counthistory.json")


def read_from_file():
    counthistory = pygrowth.counthistory.CountHistory.read("counthistory.json")
    print(counthistory)


def main():
    extract_then_save_to_file()
    read_from_file()


if __name__ == "__main__":
    main()
