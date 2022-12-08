import os
import glob
import pickle
import filetype
import csv
import numpy as np
from CS229_Final_Project.Sound_Analysis import Sound_Analysis



class Pipeline(object):

    def __init__(self, song_names=None, file_path=None, import_data=False, pipeline_filename='', obs_filename=''):
        """This __init__ for the Pipeline Class takes in a list of song_names and a file path string."""
        if not import_data:
            self.song_dictionary = dict()
            self.songs = list()
            self.path = list()
            self.list_sound_objects = list()

            if song_names  == None and file_path != None:
                song_names = list()
                file_paths = list()
                counter_list = list()
                i = 0 #number of different paths
                j = 0 #records 1st song in new path
                for file in glob.glob(file_path + '**/*.wav', recursive=True):
                    full_path = os.path.join(file_path, file)
                    song_name = os.path.basename(full_path)
                    song_path = full_path[:full_path.find(song_name)]
                    song_names.append(song_name)

                    if i == 0:
                        file_paths.append(song_path)
                        counter_list.append(1)
                        i += 1
                        song_path_old = song_path
                    else:
                        if song_path == song_path_old:
                            counter_list[len(counter_list)-1] += 1
                        else:
                            bool_continue_to_sound_object, found_path, found_songs = self.check_validity_data_import(
                                song_names[j:-1], song_path_old)
                            if bool_continue_to_sound_object:
                                self.create_sound_objects(found_songs, found_path)
                                self.songs.extend(song_names[j:-1])
                                self.path.append(found_path)
                            i += 1
                            counter_list.append(1)
                            j = len(song_names)-1
                            file_paths.append(song_path)
                            song_path_old = song_path

                #END OF LOOP
                #Need to Grab Info for the Last Set of Songs
                bool_continue_to_sound_object, found_path, found_songs = self.check_validity_data_import(
                    song_names[j:], song_path_old)
                if bool_continue_to_sound_object:
                    self.create_sound_objects(found_songs, found_path)
                    self.songs.extend(song_names[j:])
                    self.path.append(found_path)
                    self.label_dictionary = dict()
                    self.no_label_list = list()
                # getting the sets figured out
                self.num_songs_per_path = counter_list
            #FOR SINGLE CASE (SINGLE FOLDER WITH SONG NAMES)
            # Assinging Songs, Path, Sound Objs, to Self
            else:
                # Assinging Songs, Path, Sound Objs, to Self
                bool_continue_to_sound_object, found_path, found_songs = self.check_validity_data_import(
                    song_names, file_path)
                self.song_dictionary = dict()
                self.songs = found_songs
                self.path = found_path
                self.list_sound_objects = list()
                self.label_dictionary = dict()
                self.no_label_list = list()
                if bool_continue_to_sound_object:
                    self.create_sound_objects(found_songs, found_path)

        else:
            # Assinging Songs, Path, Sound Objs, to Self
            self.load_sound_objects(pipeline_filename, obs_filename)

    def check_validity_data_import(self, song_names, file_path):
        """
        :param song_names:
        :param file_path:
        :return: bool_continue_to_sound_object, found_path, found_songs
        checks the provided path and song names to make sure that path exists as well as the song names
        """
        # Some Immediate Checks for Correct Path
        if song_names is None:
            raise AttributeError("No Song Name(s) have been Selected")
        if file_path is None:
            raise AttributeError("No File Path(s) are selected")
        # More Developed  Path Checks
        strip_symbol = "\\"  # Need to get this OS specific
        flag, found_path = self.check_file_path(file_path)
        bool_continue_to_sound_object = False
        if flag == 0:
            found_songs = self.check_song_paths(found_path, song_names)
            if found_songs is not None:
                bool_continue_to_sound_object = True
        elif flag == 1:
            folders_list = found_path.strip(strip_symbol)
            found_songs = folders_list[-1]
            loc_song = found_path.find(found_songs)  # Maybe include start point
            found_path = found_path[0:loc_song]
            bool_continue_to_sound_object = True

        return bool_continue_to_sound_object, found_path, found_songs

    def check_file_path(self, file_path):
        """Checks for a valid file path. Adjusts Path as necessary (adding/removing slashes/formatting
        per Operating System)"""
        # TODO: implement logic to determine which OS you are on and to replace with proper brackets
        flag = 0
        bool_file_path = os.path.isdir(file_path)
        if not bool_file_path:
            bool_file = os.path.isfile(file_path)
            if bool_file is not None:
                file_kind = filetype.guess(file_path)
                if file_kind is None:
                    raise Exception("You have passed an unknown file into the Pipeline Class"
                                    " rather than the path variable.")
                    # Don't Need (Can't Reach)
                    # flag = -1
                    # return flag, file_path
                else:
                    if file_kind.extension == 'wav':
                        raise Warning("You have directly entered a .wav file. Processing this file.")
                        flag = 1
                        return flag, file_path
                    else:
                        raise Exception("You have passed in a " + file_kind.extension +
                                        " file which is not currently supported")
                        # Don't Need (Can't Reach)
                        # flag = -1
                        # return flag, file_path
        else:
            return flag, file_path

    def check_song_paths(self, found_path, song_names):
        """Checks if the songs exist in the desired directory marked by path"""
        # TODO: implement additional checks on sound file type
        found_songs = list()
        for song in song_names:
            check_file = found_path + song
            file_kind = filetype.guess(check_file)
            if file_kind.extension != 'wav':
                raise Warning("The Song: " + song + " is not recognized as a wav file")
            else:
                found_songs.append(song)
        return found_songs

    def create_sound_objects(self, found_songs, found_path=''):
        if found_path == '':
            sound_obj = Sound_Analysis()
            self.list_sound_objects.append(sound_obj.create_obj(found_songs))
        else:
            for song in found_songs:
                sound_obj = Sound_Analysis()
                sound_obj.create_obj(found_path + song, song)
                self.list_sound_objects.append(sound_obj)
                song_dict_len = len(self.song_dictionary)
                if song_dict_len == 0:
                    self.song_dictionary[song] = int(0)
                else:
                    self.song_dictionary[song] = int(song_dict_len)

    def load_csv_label_data(self, file_name, file_path=''):
        # Code Derived From: https://www.analyticsvidhya.com/blog/2021/08/python-tutorial-working-with-csv-file-for-data-science/
        csv_file = open(str.join(file_path, file_name))
        csv_reader = csv.reader(csv_file)
        csv_rows = list()
        label_dictionary = dict()
        no_label_list = list()
        count_stars = 0
        i = False
        for row in csv_reader:
            csv_rows.append(row)
            if i:
                try:
                    label = int(row[1])
                    label_dictionary[str(row[0])] = label
                    count_stars = 0
                except ValueError:
                    if str(row[1]) == '-':
                        no_label_list.append(str(row[0]))
                        count_stars = 0
                    if str(row[1]) == '*':
                        count_stars += 1
                    else:
                        Warning("Something Went Wrong with the CSV Import")
            else:
                i = True
        self.label_dictionary = label_dictionary
        self.no_label_list = no_label_list
        return label_dictionary, no_label_list

    def separate_data(self, label_dictionary={}, no_label_list=[]):
        if label_dictionary == {}:
            label_dictionary = self.label_dictionary
        if no_label_list == []:
            no_label_list = self.no_label_list

        indices = np.zeros(len(label_dictionary))
        indices_no_data = np.zeros(len(self.song_dictionary)-len(label_dictionary))
        i = 0
        j = 0
        for song in self.song_dictionary.keys():
            try:
                indices[i] = label_dictionary[song]
                i += 1
            except KeyError:
                indices_no_data[j] = self.song_dictionary[song]
                j += 1

        return indices, indices_no_data

    def split_test_train(self, indices, train_percent):
        if train_percent > 100:
            print("Training Percent is" + str(train_percent) + "% and is too high. ")
            train_percent = 85
            print("Training Percent set to: ")

        num_train = np.int(np.floor(indices.shape[0]*train_percent/100))
        num_test = indices.shape[0] - num_train
        indices_to_train = np.random.randint(0, np.int(indices.shape[0]), num_train)
        train_indices = indices[indices_to_train]
        test_indices = set(indices.flatten()) - set(train_indices)
        test_indices = np.array(test_indices)

        return test_indices, train_indices






    def save_sound_objects(self, song_names='', file_name='', pipeline_name=''):
        save_sound_objects = list()
        if song_names == '':
            save_sound_objects = self.list_sound_objects
        elif isinstance(song_names, (str)):
            try:
                index = self.song_dictionary[song_names]
            except KeyError:
                raise KeyError("Song Name Not in Song List")
            save_sound_objects = self.list_sound_objects[index]
        else:
            for song in song_names:
                try:
                    index = self.song_dictionary[song]
                except KeyError:
                    raise KeyError("Song Name Not in Song List")
                save_sound_objects = self.list_sound_objects[index]
        #Pickling Operation
        if file_name == '':
            file_name = "sound_objects.txt"

        save_file = open(file_name, 'wb')
        for sound_obj in save_sound_objects:
            pickle.dump(sound_obj, save_file)
        save_file.close()

        if pipeline_name == '':
            file_pipeline = "pipeline_data.txt"

        save_pipeline = open(file_pipeline, 'wb')
        pipeline_list = [self.song_dictionary, self.songs, self.path]
        pickle.dump(pipeline_list, save_pipeline)
        save_pipeline.close()
        print("Songs Saved To Local File!")


    def load_sound_objects(self, pipeline_filename, objs_filename):
        pipe_file = open(pipeline_filename, 'rb')
        pipeline_list = pickle.load(pipe_file)
        self.song_dictionary = pipeline_list[0]
        self.songs = pipeline_list[1]
        self.path = pipeline_list[2]
        pipe_file.close()

        self.list_sound_objects = list()
        with (open(objs_filename, "rb")) as openfile:
            while True:
                try:
                    self.list_sound_objects.append(pickle.load(openfile))
                except EOFError:
                    break
        print("Successfully Loaded Saved Data Into Instance Objects!")

    def return_sound_objects(self):
        return self.list_sound_objects



