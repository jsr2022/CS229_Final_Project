# Python Modules
import matplotlib.pyplot as plt


def plot(results):
    plt.savefig("plot.png")
    num_songs = results.shape[0]
    for j in range(num_songs):
        plt.scatter(j, results[j][0], color="red")
        plt.scatter(j, results[j][1], color="blue")


def plot_rms(self, rms, t):
    plt.figure()
    plt.plot(t, rms)
    plt.title(self.song_name)
    plt.xlabel("Song Time [S]")
    plt.ylabel("Normalized RMS of Volume/Intensity")
    #plt.savefig(self.song_name + ".png")
    plt.show()
