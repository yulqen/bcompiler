import argparse
import os


def get_parser():
    parser = argparse.ArgumentParser(description='Compile BICC data or prepare Excel BICC return forms.')
    parser.add_argument('-c', '--clean-datamap', dest='datamap', nargs=1, help='clean datamap file'
                                                                                     'whose path is given as string')
    parser.add_argument('-v', '--version', help='displays the current version of bcompiler', action="store_true")
    return parser


def _clean_datamap(source_file):

    CLEANED_DATAMAP_FILE = 'source_files/cleaned_datamap'
    try:
        os.remove(CLEANED_DATAMAP_FILE)
    except FileNotFoundError:
        pass
    cleaned_datamap = open(CLEANED_DATAMAP_FILE, 'a+')
    with open(source_file, 'r', encoding='UTF-8') as f:
        # make sure every line has a comma at the end
        for line in f.readlines():
            newline = line.rstrip()
            if ',' in newline[-1]:
                newline = newline + '\n'
                cleaned_datamap.write(newline)
            else:
                newline = newline + ',' + '\n'
                cleaned_datamap.write(newline)

def main():
    parser = get_parser()
    args = vars(parser.parse_args())
    if args['version']:
        print("1.0")
        return
    if args['datamap']:
        _clean_datamap(args['datamap'][0])
        print("{} cleaned".format(args['datamap'][0]))
        return


if __name__ == '__main__':
    main()