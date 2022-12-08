

def plot(results):
    plt.savefig("plot.png")
    num_songs = results.shape[0]
    for j in range(num_songs):
        plt.scatter(j, results[j][0], color="red")
        plt.scatter(j, results[j][1], color="blue")
