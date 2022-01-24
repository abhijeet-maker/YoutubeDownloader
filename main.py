import pytube
import ffmpeg
import sys
import re


def get_videos_res(url):
    # Get URL from user input
    # url=e1.get(url)
    # url=url
    get_videos_res.yt = pytube.YouTube(url)
    v_list = get_videos_res.yt.streams.order_by('resolution').desc()
    # print(v_list)
    # Append resolutions in list
    resolution = []
    for i in v_list:
        # resolution.append(str(i.resolution)+" "+str(i.fps)+"fps")
        resolution.append(str(i.resolution) + " " + str(i.fps) + "fps" + " " + str(i))
    # tk.Label(m, text="Available Resolutions").grid(row=3, column=0)

    # Data type of value inside OptionMenu
    # get_videos_res.value_inside = tk.StringVar(m)

    # Create OptionMenu
    # get_videos_res.value_inside.set("Select an Option")
    # question_menu = tk.OptionMenu(m, get_videos_res.value_inside, *resolution).grid(row=4, column=0)

    # Get the value of selected option
    # get_videos_res.val=get_videos_res.value_inside.get()

    # Button to start downloading video
    # submit_button = tk.Button(m, text='Start Downloading', command=download_videos).grid(row=5, column=0)
    print(resolution[0])

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_videos_res("https://www.youtube.com/watch?v=LXb3EKWsInQ")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
