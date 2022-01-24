import sys

import ffmpeg
import pytube
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # context = {'latest_question_list': latest_question_list}
    return render(request, 'ytdl/index.html')
    # return HttpResponse("Index Page")


def home(request):
    return render(request, 'ytdl/home.html')


def get_videos_res(request):
    url = request.GET.get('mediaurl', 'default')
    get_videos_res.yt = pytube.YouTube(url)
    print("URL: ", url)
    get_videos_res.yt = pytube.YouTube(url)
    v_list = get_videos_res.yt.streams.order_by('resolution').desc()
    # print(v_list)
    # Append resolutions in list
    resolutions = []
    get_videos_res.res_dict={}
    for i in v_list:
        res=str(i.resolution) + " " + str(i.fps) + "fps"
        get_videos_res.res_dict[res] = str(i)
    for key in get_videos_res.res_dict.keys():
        resolutions.append(key)
    return render(request, 'ytdl/get_resolution.html', {'resolution': resolutions})

#Downloaded on local server
def select_videos_res(request):
    BaseDir="download_raw"
    resolution = request.GET.get('resolution', 'default')
    resl=resolution.split('}')[0]
    itag=get_videos_res.res_dict[resl]
    itag=itag.split('<')
    itag=itag[1].split('>')[0].split()[1].split('=')[1].split('"')[1]
    print("Selected resolution: ",resl,itag)
    # Get Stream by itag
    vid = get_videos_res.yt.streams.get_by_itag(int(itag))
    # Get Title of video
    title = get_videos_res.yt.title.split()
    title = title[0]
    title = ''.join(char for char in title if char.isalpha())
    print("Title:",title)
    print("Selected Resolution: ", resl)
    if vid not in get_videos_res.yt.streams.filter(progressive=True):

        # Download video in 360p
        get_videos_res.yt.streams.get_by_itag(18).download(output_path=BaseDir + "\\\.temp", filename=title+".mp4")

        # Download Video in selected resolution
        vid.download(output_path=BaseDir + "\\\.temp" + title, filename=title+".mp4")

        # Filter audio from 360p
        stream = ffmpeg.input(BaseDir + "\\\.temp" + "\\" + title + ".mp4")
        print("stream video", stream)
        stream = stream.output(BaseDir + "\\\.temp" + "\\" + title + ".mp3", format='mp3', acodec='libmp3lame',
                               ab='320000')

        print("stream audio",stream)
        # stream=stream.output("C:\\Users\\Abhijeet\\Desktop\\PyProjects\\mp\\\.temp\\Peru_finished_audio.mp3", format='mp3', acodec='libmp3lame', ab='320000')
        #ffmpeg.run(stream, capture_stdout=True, capture_stderr=True, input=None, quiet=False, overwrite_output=True)
        #print ffmpeg error
        try:
            err,out=(ffmpeg.run(stream, cmd='venv/Lib/site-packages/ffmpeg/ffmpeg.exe', capture_stdout=True, capture_stderr=True, input=None, quiet=False, overwrite_output=True))
            print("out***********: ",out,"outerr*********: ",err)
        except ffmpeg.Error as e:
            print("err*********:" ,e.stderr, file=sys.stderr)
        # If stream is progressive

    else:
        #title=title+".mp4"
        vid.download(output_path=BaseDir, filename=title)
    file=BaseDir+"/"+title
    print("file",file)
    select_videos_res.title=title
    return render(request, 'ytdl/download.html/', {'file': file, 'title': title})

#serve over client now
def download(request):
    document_root = settings.MEDIA_ROOT
    print("Media root",document_root)
    BaseDir = "download_raw"
    file_path = BaseDir + "/" + select_videos_res.title
    print("file_path",file_path)
    #file_path = os.path.join(settings.MEDIA_ROOT, path)
    with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.rar")
            response['Content-Disposition'] = 'inline; filename=' + file_path +".mp4"
            return response
    return render(request, 'ytdl/download_completed.html')


def download_completed(request):
    return render(request, 'ytdl/index.html')