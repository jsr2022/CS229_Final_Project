# Python Modules
import matplotlib.pyplot as plt
import librosa
import librosa.display

def plot(results):
    plt.savefig("plot.png")
    num_songs = results.shape[0]
    for j in range(num_songs):
        plt.scatter(j, results[j][0], color="red")
        plt.scatter(j, results[j][1], color="blue")


def plot_rms(self, rms, t):
    plt.figure()
    plt.plot(t, rms)
    plt.title(self.song_name.strip)
    plt.xlabel("Song Time [S]")
    plt.ylabel("Normalized RMS of Volume/Intensity")
    #plt.savefig(self.song_name + ".png")
    plt.show()

def plot_pitch(chroma_cq):
    plt.plot()
    img = librosa.display.specshow(chroma_cq, y_axis='chroma', x_axis='time')
    plt.colorbar(img)
    plt.show()
    plt.savefig("chroma.png")

    fig, ax = plt.subplots(nrows=2, sharex=True, sharey=True)

    img = librosa.display.specshow(chroma_cq, y_axis='chroma', x_axis='time', ax=ax[0])
    ax[0].set(title='chroma_cq')
    ax[0].label_outer()
    librosa.display.specshow(chroma_cens, y_axis='chroma', x_axis='time', ax=ax[1])
    ax[1].set(title='chroma_cens')
    fig.colorbar(img, ax=ax)
