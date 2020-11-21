import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import Rectangle

global ax

def update_heatmap(data):
    global ax
    ax = sns.heatmap(data, annot = True, cbar = False)

def highlight(ax, y, x):
    ax.add_patch(Rectangle((x, y), 1, 1, fill=True, edgecolor='cyan', lw=3))

def animate_heat_map(str1, str2):
    global ax
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

def trace_back(data, m, n):
    global ax

    while (m != 0 or n != 0):
        left = data[m][n - 1]
        top = data[m - 1][n]
        left_top = data[m - 1][n - 1]

        min_square = min(left, top, left_top)
        if left_top == min_square:
            highlight(ax, m - 1, n - 1)
            m -= 1
            n -= 1
        
        elif left == min_square:
            highlight(ax, m, n - 1)
            n -= 1
        
        else:
            highlight(ax, m - 1, n)
            m -= 1

        plt.pause(0.1)
    return

 
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
            
            if j % 5 == 0:
                update_heatmap(data)
                plt.pause(0.1)
                plt.clf()

            if i == m and j == n:
                update_heatmap(data)
                global ax
                highlight(ax, m, n)
                trace_back(data, m, n)

                plt.pause(50)
                 
            # plt.pause(0.00001) 
            # plt.clf()  



    return data[m][n]


if __name__ == "__main__":
    str1 = "optional"
    str2 = "eptoinally"

    animate_heat_map(str1, str2)
    editDistDP(str1, str2)
    