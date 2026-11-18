input_files = [path + file for (root, dirs, files) in os.walk(path) 
                                        for file in files if file.endswith('.pbxproj')]
