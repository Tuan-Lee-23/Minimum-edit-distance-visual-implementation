import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def update_heatmap(data):
    ax = sns.heatmap(data, annot = True, cbar = False)




def animate_heat_map(str1, str2):
    fig = plt.figure(figsize = (12, 8))

    nx = ny = 5
    data = np.array([[0, 0, 0],
                     [0, 0, 0],
                     [0, 0, 0]])
    update_heatmap(data)
    def init():
        plt.clf()
        update_heatmap(data)

    def animate(i):
        plt.clf()

        data = np.array([[0, 0, 0],
                            [0, 0, 0],
                            [0, 0, 0]])

        data2 = np.array([[1, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0]])
    

        data3 = np.array([[0, 1, 0],
                        [0, 0, 0],
                        [0, 0, 0]])

        data4 = np.array([[0, 0, 1],
                        [0, 0, 0],
                        [0, 0, 0]])
        update_heatmap(data)
        plt.pause(0.5)

        update_heatmap(data2)
        plt.pause(0.5)

        update_heatmap(data3)
        plt.pause(0.5)

        update_heatmap(data4)

    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=1000)

    plt.tight_layout()
    plt.show()


 
def editDistDP(str1, str2):
    m, n = len(str1), len(str2)

    # Create a table to store results of subproblems
    dp = np.array([[0 for x in range(n + 1)] for x in range(m + 1)])
    
 
    # Fill d[][] in bottom up manner
    for i in range(m + 1):
        for j in range(n + 1):
 
            # If first string is empty, only option is to
            # insert all characters of second string
            if i == 0:
                dp[i][j] = j    # Min. operations = j
 
            # If second string is empty, only option is to
            # remove all characters of second string
            elif j == 0:
                dp[i][j] = i    # Min. operations = i
 
            # If last characters are same, ignore last char
            # and recur for remaining string
            elif str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]
 
            # If last character are different, consider all
            # possibilities and find minimum
            else:
                dp[i][j] = 1 + min(dp[i][j-1],        # Insert
                                   dp[i-1][j],        # Remove
                                   dp[i-1][j-1])    # Replace
                print(i, j)
        print(dp)

    return dp[m][n]


if __name__ == "__main__":
    str1 = "optional"
    str2 = "eptoinally"

    animate_heat_map(str1, str2)
    editDistDP(str1, str2)
    