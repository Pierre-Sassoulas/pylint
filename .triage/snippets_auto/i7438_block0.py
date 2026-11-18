input_files = []
for root, dirs, files in os.walk(path):
             for file in files:
                 if file.endswith(".pbxproj"):
                     input_files.append(path + file)
