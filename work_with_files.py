def safe_images(url, path, params=None):
    filename = path
    with open(filename, 'wb') as file:
        file.write(requests.get(url, params=params).content)


def define_filetype(url):
    url_path = urlparse(url).path
    fyletype = os.path.splitext(url_path)[1]
    return fyletype


def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

