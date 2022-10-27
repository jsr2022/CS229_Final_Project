# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from CS229_Final_Project.Pipeline import Pipeline


def print_hi(name):
    #TIPS for pushing and pulling to the main set
    #MUST COMMIT TO YOUR LOCAL (MINE IS MAIN LOCAL) first
    #Steps to Push a File all the way to the github branch (jsr_branch)
    #   1) Add All Desired Files to Local Branch
    #       i)This is where you will describe your changes
    #   2) Go into push menu and select the branch (jsr_branch)
    #   3) Select what you would like to push to that branch
    #   4) Push it up!
    #Steps to pull
    #   1) Go to git options and select
    #   2) Pick which branch you would like to pull from (jsr_branch/main)
    #   3) pull from there
    #Steps to Update
    #select update and generally the merge step is best
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #print_hi('PyCharm')
    file_path = r"C:\Users\jonat\PycharmProjects\CS229_Final_Project\CS229_Final_Project\Music_Wavs\Vladimir Horowitz\Horowitz - The Last Recording\\"
    song_name = ["01 Haydn- Piano Sonata #59 In E Flat, H 16-49 - 1. Allegro.wav"]
    p1 = Pipeline(song_name, file_path)
    print(p1.list_sound_objects[0].attributes)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
