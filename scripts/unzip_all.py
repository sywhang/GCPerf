import os, zipfile

def unzip_all_directory(directory):
    print('Searching for zip files in ' + directory)
    for filename in os.listdir(directory):
        pathname = os.path.join(directory, filename)
        if filename.endswith(".zip") and not os.path.isdir(pathname):
            print('Unzipping zip file: ' + pathname)
            name = os.path.splitext(os.path.basename(pathname))[0]
            if not os.path.isdir(pathname):
                zip = zipfile.ZipFile(pathname)
                if not os.path.isdir(os.path.join(directory, name)):
                    os.mkdir(os.path.join(directory, name))
                zip.extractall(path=os.path.join(directory, name))
        elif os.path.isdir(pathname):
            print('Recursively searching through ' + pathname)
            unzip_all_directory(pathname)


unzip_all_directory("E:/GC/Traces/suwhang-test-2")
