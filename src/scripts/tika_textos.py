import sys
from tika import parser


class tika_textos:
    def __init__(self):
        pass

    def process_file(self, filepath):
        file_data = parser.from_file(filepath)
        return file_data["content"].strip()


def main(filepath):
    t = tika_textos()
    print(t.process_file(filepath))


if __name__ == "__main__":
    main(sys.argv[1])
