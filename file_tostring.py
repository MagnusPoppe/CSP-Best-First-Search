def read_file_to_string(path):
    # Reading file:
    file = open(path)
    file_to_string = ""
    for line in file: file_to_string += line
    file.close()
    return file_to_string