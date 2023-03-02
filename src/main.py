from huffman import Huffman
import ast
import os.path
import ntpath


def get_file_name(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def get_base_folder(path):
    return os.path.dirname(path)


def path_exists(file_path):
    return os.path.exists(file_path)


if __name__ == "__main__":
    print("\n")
    print("HUFFMAN COMPRESSION AND DECOMPRESSION FOR TEXT FILES")
    print("\n")
    print("1 - Compress")
    print("0 - Decompress")
    print("Any Key - Exit")
    print("\n")

    user = 0

    huff = Huffman()
    while user == 1 or user == 0:

        user = int(input("Do you want to compress or decompress? "))

        if user == 1:
            file_path = input("Enter file path: ")

            if not path_exists(file_path):
                print("Invalid file path")
                continue

            if file_path.split(".")[-1] != "txt":
                print("Please insert a TEXT FILE")
                continue

            file_name = get_file_name(path=file_path).split(".")[0]

            base_folder = get_base_folder(file_path)

            with open(file_path, 'r') as file:
                data = huff.compress(file.read())  # Compress given file

            with open(f"{base_folder}/{file_name}_compressed.bin", 'wb') as file:
                # Output the compressed data into a new binary file
                data["encoded"].tofile(file)

            with open(f"{base_folder}/{file_name}_utils.txt", 'w') as file:
                # Save the utilities(code table, padding) in another file
                file.write(str(data["utils"]))

            print("\n")
            print("File successfully compressed!!!")
            print("\n")

        elif user == 0:
            compressed_file_path = input("Enter compressed binary file path: ")

            if not path_exists(compressed_file_path):
                print("Invalid compressed file path")
                continue

            if compressed_file_path.split(".")[-1] != "bin":
                print("Please insert a BINARY COMPRESSED FILE")
                continue

            utils_path = input("Enter utils file path: ")

            if not path_exists(utils_path):
                print("Invalid utils file path")
                continue

            if utils_path.split(".")[-1] != "txt":
                print("Please insert a valid UTILITY FILE")
                continue

            file_name = get_file_name(compressed_file_path).split(".")[
                0].split("_")[0]

            base_folder = get_base_folder(compressed_file_path)

            try:
                with open(utils_path, 'r') as file_utils, open(compressed_file_path, 'rb') as file_compressed:
                    # Decompress the compressed file
                    decompressed = huff.decompress(
                        utils=ast.literal_eval(file_utils.read()), file=file_compressed)

                with open(f"{base_folder}/{file_name}.txt", "w") as file_uncomp:
                    # Output the decompressed data to a new file
                    file_uncomp.write(decompressed)

                print("\n")
                print("File successfully decompressed!!!")
                print("\n")

            except ValueError:
                print("Invalid binary or utility file")
                print("Please insert valid binary and utility files")
                continue

        else:
            break
