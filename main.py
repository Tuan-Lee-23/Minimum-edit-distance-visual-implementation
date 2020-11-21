import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def update_heatmap(data):
    ax = sns.heatmap(data, annot = True, cbar = False)


def animate_heat_map(str1, str2):
    fig = plt.figure(figsize = (12, 8))

    m, n = len(str1), len(str2)
    dp = np.array([[0 for x in range(n + 1)] for x in range(m + 1)])
    update_heatmap(dp)

    def init():
        plt.clf()
        update_heatmap(dp)

    def animate():
        plt.clf()
        editDistDP(str1, str2)


    anim = animation.FuncAnimation(fig, animate, init_func = init, interval = 1)

    plt.tight_layout()


 
def editDistDP(str1, str2):
    m, n = len(str1), len(str2)

    # Create a table to store results of subproblems
    data = np.array([[0 for x in range(n + 1)] for x in range(m + 1)])
    
 
    # Fill d[][] in bottom up manner
    for i in range(m + 1):
        for j in range(n + 1):

            # If first string is empty, only option is to
            # insert all characters of second string
            if i == 0:
                data[i][j] = j    # Min. operations = j
 
            # If second string is empty, only option is to
            # remove all characters of second string
            elif j == 0:
                data[i][j] = i    # Min. operations = i
 
            # If last characters are same, ignore last char
            # and recur for remaining string
            elif str1[i-1] == str2[j-1]:
                data[i][j] = data[i-1][j-1]
 
            # If last character are different, consider all
            # possibilities and find minimum
            else:
                data[i][j] = 1 + min(data[i][j-1],        # Insert
                                   data[i-1][j],        # Remove
                                   data[i-1][j-1])    # Replace
            update_heatmap(data)

            if i == m and j == n:
                plt.pause(50)
            plt.pause(0.000005)
            plt.clf()    

    goal = data[m][n] 




    return data[m][n]


if __name__ == "__main__":
    str1 = "optional"
    str2 = "eptoinally"

    animate_heat_map(str1, str2)
    editDistDP(str1, str2)
    