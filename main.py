import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import Rectangle

global ax

def update_heatmap(data, str1, str2):
    global ax
    sns.set(font_scale = 1.4)
    ax = sns.heatmap(data, annot = True, cbar = False)

    tick_x = list(str2)
    tick_y = list(str1)

    tick_x.insert(0, '')
    tick_y.insert(0, '')

    # decrease xticks top padding
    # ax.tick_params(axis = 'x', which = 'major', pad = -80)

    # Move xticks to top
    ax.xaxis.set_ticks_position('top')

    plt.xticks(range(len(tick_x)), tick_x, rotation = 0)
    plt.yticks(range(len(tick_y)), tick_y, rotation = 0)

    plt.xticks(plt.xticks()[0] + 0.5)
    plt.yticks(plt.yticks()[0] + 0.5)

    plt.tick_params(axis = "both", which = "both", left = False, top = False)

    
def highlight(ax, y, x, color = 'cyan'):
    if color == 'cyan':
        edgec = 'cyan'
    elif color == 'red':
        edgec = 'lime'
    ax.add_patch(Rectangle((x, y), 1, 1, edgecolor= edgec, lw= 2))

def animate_heat_map(str1, str2):
    global ax
    fig = plt.figure(figsize = (12, 8))

    m, n = len(str1), len(str2)
    dp = np.array([[0 for x in range(n + 1)] for x in range(m + 1)])
    update_heatmap(dp, str1, str2)

    def init():
        plt.clf()
        update_heatmap(dp, str1, str2)

    def animate(i):
        plt.clf()
        editDistDP(str1, str2)

        plt.clf()
        lables = np.array([['a', 'b', 'c' ,'d'], ['d', 'c', 'b', 'a']])
        data = np.empty((2, 4))
        sns.heatmap(data, annot = lables, cbar = False, fmt = '')

        plt.pause(5)


    anim = animation.FuncAnimation(fig, animate, init_func = init, interval = 0)

    plt.tight_layout()
    plt.show()

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

        plt.pause(0.3)

        # move down: delete
        # move right: insert
        # move diag: +1 --> replace
        # move diag: +0 --> nothing
    return

 
def editDistDP(str1, str2):
    m, n = len(str1), len(str2)
    global ax

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
                high = np.argmin(np.array([data[i][j - 1], data[i - 1][j], data[i - 1][j - 1]]))
 
                if high == 0:
                    update_heatmap(data, str1, str2)
                    highlight(ax, i, j - 1)
                    highlight(ax, i, j, 'red')
                elif high == 1:
                    update_heatmap(data, str1, str2)
                    highlight(ax, i - 1, j)
                    highlight(ax, i, j, 'red')
                else:
                    update_heatmap(data, str1, str2)
                    highlight(ax, i - 1, j - 1)
                    highlight(ax, i, j, 'red')
                plt.pause(0.1)
            
            # if j % 5 == 0:
            update_heatmap(data, str1, str2)
            plt.pause(0.0005)
            plt.clf()

            if i == m and j == n:
                update_heatmap(data, str1, str2)
                # global ax
                highlight(ax, m, n)
                trace_back(data, m, n)

                plt.pause(2)
                 
            # plt.pause(0.00001) 
            # plt.clf()  
    return data[m][n]


if __name__ == "__main__":
    str1 = "optioonal"
    str2 = "optional"

    animate_heat_map(str1, str2)
    # editDistDP(str1, str2)
    