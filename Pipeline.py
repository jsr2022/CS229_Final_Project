import os.path
import filetype
from CS229_Final_Project.Sound_Analysis import Sound_Analysis


class Pipeline(object):

    def __init__(self, song_names=None, file_path=None):
        """This __init__ for the Pipeline Class takes in a list of song_names and a file path string."""
        # Some Immediate Checks for Correct Path
        if song_names is None:
            raise AttributeError("No Song Name(s) have been Selected")
        if file_path is None:
            raise AttributeError("No File Path(s) are selected")
        # More Developed  Path Checks
        strip_symbol = "\\" # Need to get this OS specific
        flag, found_path = self.check_file_path(file_path)
        bool_continue_to_sound_object = False
        if flag == 0:
            found_songs = self.check_song_paths(found_path, song_names)
            if found_songs is not None:
                bool_continue_to_sound_object = True
        elif flag == 1:
            folders_list = found_path.strip(strip_symbol)
            found_songs = folders_list[-1]
            loc_song = found_path.find(found_songs) # Maybe include start point
            found_path = found_path[0:loc_song]
            bool_continue_to_sound_object = True

        # Assinging Songs, Path, Sound Objs, to Self
        self.songs = found_songs
        self.path = found_path
        self.list_sound_objects = list()
        if bool_continue_to_sound_object:
            self.create_sound_objects(found_songs, found_path)


    def check_file_path(self, file_path):
        """Checks for a valid file path. Adjusts Path as necessary (adding/removing slashes/formatting
        per Operating System)"""
        # TODO: implement logic to determine which OS you are on and to replace with proper brackets
        flag = 0
        bool_file_path = os.path.isdir(file_path)
        if not bool_file_path:
            bool_file = os.path.isfile()
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
        sound_obj = Sound_Analysis()
        if found_path == '':
            self.list_sound_objects.append(sound_obj.create_obj(found_songs))
        else:
            for song in found_songs:
                sound_obj.create_obj(found_path + song, song)
                self.list_sound_objects.append(sound_obj)

    def return_sound_objects(self):
        return self.list_sound_objects



