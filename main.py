# Custom Files
from CS229_Final_Project.Pipeline import Pipeline
from CS229_Final_Project import processing
from CS229_Final_Project import Output_Calls
# Python Modules
import numpy as np
import csv


# TIPS for pushing and pulling to the main set
# MUST COMMIT TO YOUR LOCAL (MINE IS MAIN LOCAL) first
# Steps to Push a File all the way to the github branch (jsr_branch)
#   1) Add All Desired Files to Local Branch
#       i)This is where you will describe your changes
#   2) Go into push menu and select the branch (jsr_branch)
#   3) Select what you would like to push to that branch
#   4) Push it up!
# Steps to pull
#   1) Go to git options and select
#   2) Pick which branch you would like to pull from (jsr_branch/main)
#   3) pull from there
# Steps to Update
# select update and generally the merge step is best
# Use a breakpoint in the code line below to debug your script.
# Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':

    initial_data_loading = False
    save_csv = False

    # Saving All Pre-Trained Analysis Objects
    analysis_filename = 'updated_sound_analysis.dont_open'
    pipeline_filename = 'pipline2.dont_open'

    if initial_data_loading:
        # File Path to All .wav files (63 total 33 with labels and 30 with no labels)
        file_path = r"C:\Users\jonat\OneDrive - Stanford\Music\\"
        # Performing Pre-Training Analysis
        p1 = Pipeline(file_path=file_path)
        p1.save_sound_objects(song_names='', file_name=analysis_filename, pipeline_name=pipeline_filename)

        # Saving or Not Saving Song_Difficulty.csv File with all the song names
        # This is used to help speed up data collection as we manually pulled the labels from henle
        if save_csv:
            p2 = Pipeline(import_data=True, pipeline_filename=pipeline_filename, obs_filename=analysis_filename)
            # Following CSV Code Derived From: https://www.pythontutorial.net/python-basics/python-write-csv-file/
            header = ['Song_Names', 'Song_Difficulty']
            with open('Song_Difficulty2.csv', 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                # write the header
                writer.writerow(header)
                # write multiple rows
                all_song_names = ""
                for key in p2.song_dictionary.keys():
                    writer.writerow([str(key)])
            f.close()

    # Loading Data Back Into RAM
    p2 = Pipeline(import_data=True, pipeline_filename=pipeline_filename, obs_filename=analysis_filename)
    # Loading in the Song_Difficulty.csv into the set and associating the songs with their labels as well as a list of
    # songs with no labels
    label_dictionary, no_label_list = p2.load_csv_label_data(file_path='', file_name="Song_Difficulty.csv")
    # Associating the indices of song objects with labels and no labels
    indices, indices_no_data = p2.separate_data()

    # Splitting the indices with labels into training and testing sets
    train_percent = 80
    test_indices, train_indices = p2.split_test_train(indices, train_percent)

    # ---------TRAINING and TESTING---------
    # Important Constants
    vol_max = 1000
    vol_num_ranges = 100
    pitch_num_ranges = 20
    learning_rate = 0.01
    linear_bound = 0.5e-3
    poly_bound = 0.5e-3

    # ---------TRAINING---------
    songs = p2.list_sound_objects
    train = np.zeros([len(train_indices), vol_num_ranges + pitch_num_ranges])
    train_labels = np.zeros(len(train_indices))
    for i in range(len(train_indices)):
        index = train_indices[i]
        train_labels[i] = label_dictionary[songs[index].song_name]

        temp = songs[index].librosa_rms_norm
        rms = temp.flatten()
        rms_normalized = rms[0::10]
        pitch_delt = songs[index].chroma_max_dat
        vol_delt = processing.delta_volume(rms_normalized)
        pitch_dist = processing.get_pitch_dist(pitch_delt, pitch_num_ranges, 1)
        vol_dist = processing.get_vol_dist(vol_delt, vol_num_ranges, vol_max)

        train[i] = processing.feature(vol_dist, pitch_dist)

    # ---------TESTING---------
    test = np.zeros([len(test_indices), vol_num_ranges + pitch_num_ranges])
    test_labels = np.zeros(len(test_indices))
    for j in range(len(test_indices)):
        index = test_indices[j]
        test_labels[j] = label_dictionary[songs[index].song_name]

        temp = songs[index].librosa_rms_norm
        rms = temp.flatten()
        rms_normalized = rms[0::10]
        pitch_delt = songs[index].chroma_max_dat
        vol_delt = processing.delta_volume(rms_normalized)
        pitch_dist = processing.get_pitch_dist(pitch_delt, pitch_num_ranges, 1)
        vol_dist = processing.get_vol_dist(vol_delt, vol_num_ranges, vol_max)

        test[j] = processing.feature(vol_dist, pitch_dist)

    # Adding Intercept to Test Data (already added)!
    test_linear = np.append(np.ones((test.shape[0], 1)), test, axis=1)

    # ---------RUNNING ACTUAL ALGORITHMS---------
    # Regular Regression
    theta_linear = processing.linear_regression(train, train_labels, learning_rate, linear_bound)
    # Poly Prediction
    theta_poly = processing.poly_regression(train, train_labels, learning_rate, poly_bound)

    header = ['Theta Linear']

    with open('theta_linear1.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(header)
        # write multiple rows
        all_song_names = ""
        for i in range(len(theta_linear)):
            writer.writerow([str(theta_linear[i])])
    f.close()

    header = ['Theta Polynomial']
    with open('theta_polynomial1.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(header)
        # write multiple rows
        all_song_names = ""
        for i in range(len(theta_poly)):
            writer.writerow([str(theta_poly[i])])
    f.close()



    print("Test Results")
    data_stuff = list()
    res_arr = np.zeros((len(test_indices), 5))
    res_stats = np.zeros((4,2))
    for k in range(len(test_indices)):
        index = test_indices[k]
        song = songs[index].song_name
        linear_predict = np.dot(theta_linear, test_linear[k])
        poly_predict = np.dot(theta_poly, processing.monomialize_single(test[k]))

        res_arr[k, 0] = linear_predict
        res_arr[k, 1] = poly_predict
        res_arr[k, 2] = test_labels[k]
        res_arr[k, 3] = np.abs(linear_predict-test_labels[k])/test_labels[k]*100
        res_arr[k, 4] = np.abs(poly_predict - test_labels[k]) / test_labels[k]*100


        data_stuff.append([song, test_labels[k], linear_predict, poly_predict])
        print("Linear Reg " + str(song) + " predicted result: " + str(linear_predict) + " actual result: " + str(test_labels[k]))
        print("Poly Reg   " + str(song) + " predicted result: " + str(poly_predict) + " actual result: " + str(test_labels[k]))
    print(" ")

    res_stats[0, 0] = np.abs(np.mean(res_arr[:, 0]-res_arr[:, 2]))  # Linear Mean Error
    res_stats[0, 1] = np.abs(np.mean(res_arr[:, 1]-res_arr[:, 2]))  # Poly Mean Error
    res_stats[1, 0] = np.mean(res_arr[:, 3])  # Linear Mean % Error
    res_stats[1, 1] = np.mean(res_arr[:, 4])  # Poly Mean % Error

    res_stats[2, 0] = np.sqrt(np.var(res_arr[:, 0]-res_arr[:, 2])) # Linear STD
    res_stats[2, 1] = np.sqrt(np.var(res_arr[:, 1]-res_arr[:, 2])) # Poly STD
    res_stats[3, 0] = np.sqrt(np.var(res_arr[:, 3])) # Linear % STD
    res_stats[3, 1] = np.sqrt(np.var(res_arr[:, 4]))  # Poly % STD


    print("Linear Regression Results:")
    print("Mean Error: " + str(res_stats[0, 0]))
    print("Percent Mean Error: " + str(res_stats[1, 0]))
    print("Standard Deviation: " + str(res_stats[2, 0]))
    print("Percent Standard Deviation: "+ str(res_stats[3, 0]))
    print(" ")
    print("Polynomial Regression Results:")
    print("Mean Error: " + str(res_stats[0, 1]))
    print("Percent Mean Error: " + str(res_stats[1, 1]))
    print("Standard Deviation: " + str(res_stats[2, 1]))
    print("Percent Standard Deviation: "+ str(res_stats[3, 1]))
    a = "line used to place break statement"

    Output_Calls.plot_pitch(songs[index].chroma_cq)

    #---------OLD CODE---------

    # plot
    # plt.scatter(1, np.dot(theta, processing.monomialize_single(test1)), color='red')
    #plt.savefig("plot.png")

    # regular prediction
    # theta = processing.linear_regression(train, labels, 0.01)
    # print(np.dot(theta, test1))
    # print(np.dot(theta, test2))

    #p1 = Pipeline(song_name, file_path)
    #p1.list_sound_objects[:].song_name
    #p1.save_sound_objects()

    #'\n'.join({key} for key in p2.song_dictionary.keys())
    #print(p2.song_dictionary.keys())

    #print(p2.list_sound_objects[8].song_name)
    #print(p2.list_sound_objects[9].song_name)
    # print(p2.song_dictionary)
    # print(p2.list_sound_objects[0].librosa_rms_norm)
    # print(p2.list_sound_objects)

    #print_hi('PyCharm')
    # file_path = r"C:\Users\jonat\PycharmProjects\CS229_Final_Project\CS229_Final_Project\Music_Wavs\Vladimir Horowitz\Horowitz - The Last Recording\\"
    # sn1 = "01 Haydn- Piano Sonata #59 In E Flat, H 16-49 - 1. Allegro.wav"
    # sn2 = "02 Haydn- Piano Sonata #59 In E Flat, H 16-49 - 2. Adagio E Cantabile.wav"
    # sn3 = "03 Haydn- Piano Sonata #59 In E Flat, H 16-49 - 3. Finale- Tempo Di Minuet.wav"
    # sn4 = "04 Chopin- Mazurka #3 In E, Op. 6-3.wav"
    # sn5 = "05 Chopin- Nocturne #16 In E Flat, Op. 55-2.wav"
    # sn6 = "06 Chopin- Impromptu #4 In C Sharp Minor, Op. 66, 'Fantaisie-Impromptu'.wav"
    # sn7 = "07 Chopin- Etude #1 In A Flat, Op. 25-1, 'Aeolian Harp'.wav"
    # sn8 = "08 Chopin- Etude #5 In E Minor, Op. 25-5.wav"
    # sn9 = "09 Chopin- Nocturne #17 In B, Op. 62-1.wav"
    # sn10= "10 Liszt- Weinen, Klagen, Sorgen, Zagen.wav"
    # song_name = [sn1, sn2, sn3, sn4, sn5, sn6, sn7, sn8, sn9, sn10]

