# RENDERING FILES SUCH AS IMAGES, CSS, ETC
def render_file(file_path):
    print(f"Requested file {file_path}")

    file_path = file_path[1:len(file_path)]

    with open(file_path, 'r') as f:
        file_string = f.read()

    return file_string

