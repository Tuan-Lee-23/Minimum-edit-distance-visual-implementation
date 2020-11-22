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
    edgec = ''
    if color == 'cyan':
        edgec = 'cyan'
    elif color == 'red':
        edgec = 'lime'
    elif color == 'lime':
        edgec = 'red'
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
        # plt.clf()
        result, states = editDistDP(str1, str2)
        # states = [0, 0, 0, 0, 1, 3, 2, 1, 1]

        plt.clf()
        str1_temp = ""
        str2_temp = ""

        if len(str2) > len(str1):
            str1_temp = str1.ljust(len(str2))
            str2_temp = str2
        elif len(str1) > len(str2):
            str2_temp = str2.ljust(len(str1))
            str1_temp = str1
        
        ls_str1 = np.array(list(str1_temp), dtype = np.dtype('U10'))
        ls_str2 = np.array(list(str2_temp), dtype = np.dtype('U10'))

        
        labels = np.array([ls_str1, ls_str2])

        data = np.ones((2, len(ls_str2)))
        data[1, :] = 10

        ax2 = sns.heatmap(data, annot = labels, cbar = False, fmt = '')
        # plt.pause(5)
        plt.pause(0.1)

        # test
        for i, state in enumerate(states):
            if state == 0:
                highlight(ax2, 0, i)
            else:
                highlight(ax2, 0, i, 'red')
                ax2 = sns.heatmap(data, annot = labels, cbar = False, fmt = '')
                plt.pause(0.3)

                plt.clf()
                if state == 1:
                    labels[0, i] += ' (replace)'
                elif state == 2:
                    labels[0, i] += ' (insert)'
                elif state == 3:
                    labels[0, i] += ' (delete)'

        
            ax2 = sns.heatmap(data, annot = labels, cbar = False, fmt = '')
            
            plt.pause(0.5)
            plt.clf()
            ax2 = sns.heatmap(data, annot = labels, cbar = False, fmt = '')

        plt.pause(7)
        plt.close('all')


    anim = animation.FuncAnimation(fig, animate, init_func = init, interval = 0)

    plt.tight_layout()
    plt.show()

def trace_back(data, m, n):
    global ax
    states = []

    while (m != 0 or n != 0):
        left = data[m][n - 1]
        top = data[m - 1][n]
        left_top = data[m - 1][n - 1]

        min_square = min(left, top, left_top)
        if left_top == min_square:
            if left_top == data[m, n]:
                states.append(0)
            elif left_top == data[m, n] - 1:
                states.append(1)

            highlight(ax, m - 1, n - 1)
            m -= 1
            n -= 1

        elif left == min_square:
            states.append(2)
            highlight(ax, m, n - 1)
            n -= 1
        
        else:
            states.append(3)
            highlight(ax, m - 1, n)
            m -= 1

        plt.pause(0.3)

        # move down: delete (3)
        # move right: insert (2)
        # move diag: +1 --> replace (1)
        # move diag: +0 --> nothing (0)

    states = states[::-1]
    return states

 
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

                update_heatmap(data, str1, str2)
                if high == 0:

                    highlight(ax, i, j - 1)
                    highlight(ax, i, j, 'red')
                elif high == 1:
                    highlight(ax, i - 1, j)
                    highlight(ax, i, j, 'red')
                else:
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
                highlight(ax, m, n, 'lime')
                states = trace_back(data, m, n)

                plt.pause(5)
                 
    return [data[m][n], states]


if __name__ == "__main__":
    str1 = "optioonal"
    str2 = "optional"

    animate_heat_map(str1, str2)
    