import sys

import ffmpeg
import pytube
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
import subprocess

# Create your views here.
from YoutubeDL.settings import BASE_DIR


def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # context = {'latest_question_list': latest_question_list}
    return render(request, 'ytdl/index.html')
    # return HttpResponse("Index Page")


def home(request):
    return render(request, 'ytdl/home.html')


def get_videos_res(request):
    url = request.GET.get('mediaurl', 'default')
    yt = pytube.YouTube(url)
    print("URL: ", url)
    yt = pytube.YouTube(url)
    v_list = yt.streams.order_by('resolution').desc()
    # print(v_list)
    # Append resolutions in list
    resolutions = {}
    for i in v_list:
        res = str(i.resolution) + " " + str(i.fps) + "fps"
        resolutions[res] = str(i)
    print("yt:", yt)
    return render(request, 'ytdl/get_resolution.html', {'resolution': resolutions, 'youtube': yt, 'url': url})


#Merge Audi Video
def merge_audio_video(video,audio,output):
    input_video = ffmpeg.input(video)
    input_audio = ffmpeg.input(audio)
    codec = "copy"
    outputfile=output


    #subprocess.run("ffmpeg -i video.mp4 -i audio.mp4 -c copy output.mp4")
    #stream = ffmpeg.concat(input_video, input_audio, v=1, a=1)
    #.output(<video_name>, vcodec="copy", acodec="copy ")
    #stream=ffmpeg.output(input_video, input_audio, output, vcodec="copy")
    #comp=ffmpeg.compile(stream, cmd=BaseDir+'/ffmpeg/bin/ffmpeg')
    #print(comp)
    try:
        #print(comp)
        subprocess.run(f"ffmpeg -i {input_video} -i {input_audio} -c {codec} {outputfile}")
        #ffmpeg.run(stream, cmd="binary/ffmpeg.exe", capture_stdout=True, capture_stderr=True, input=None, quiet=False, overwrite_output=True)
    except ffmpeg.Error as e:
        #print('stdout:', e.stdout.decode('utf8'))
        print('stderr:', e.stderr.decode('utf8'))
        raise e
    return("Video Downloaded Sucessfully")
#Downloaded on local server
def select_videos_res(request):
    BaseDir = "download_raw"
    resolution = request.GET.get('resolution', 'default')
    print("*************", resolution)
    url = resolution.split(",")[2]
    yt = pytube.YouTube(url)
    itag = resolution.split('itag="')[1]
    resolution = resolution.split("<")[0]
    itag = itag.split('"')[0]
    # Get Stream by itag
    vid = yt.streams.get_by_itag(int(itag))
    yt.streams.get_by_itag(int(itag)).download()
    #yt.streams.get_by_itag(18).download
    # Get Title of video
    title = yt.title.split()
    title = title[0]
    title = ''.join(char for char in title if char.isalpha())
    index.title=title
    print("Title:",title)
    print("Selected Resolution: ",resolution )
    if vid not in yt.streams.filter(progressive=True):

        # Download video in 360p
        yt.streams.get_by_itag(18).download(output_path=BaseDir + "\\\.temp", filename=title+".mp4")

        # Download Video in selected resolution
        vid.download(output_path=BaseDir + "\\\.temp" + title, filename=title+".mp4")

        # Filter audio from 360p
        input_video=BaseDir + "\\\.temp" + "\\" + title + ".mp4"
        #stream = ffmpeg.input(BaseDir + "\\\.temp" + "\\" + title + ".mp4")
        #print("stream video", stream)
        #stream = stream.output(BaseDir + "\\\.temp" + "\\" + title + ".mp3", format='mp3', acodec='libmp3lame',ab='320000')
        outputfile=BaseDir + "\\\.temp" + "\\" + title + ".mp3"
        file="mp3"
        codec="libmp3lame"
        bitrate=320000
        #print("stream audio",stream)

        # stream=stream.output("C:\\Users\\Abhijeet\\Desktop\\PyProjects\\mp\\\.temp\\Peru_finished_audio.mp3", format='mp3', acodec='libmp3lame', ab='320000')
        #ffmpeg.run(stream, capture_stdout=True, capture_stderr=True, input=None, quiet=False, overwrite_output=True)
        #print ffmpeg error
        try:
            subprocess.run(f"ffmpeg -i {input_video} -vn -f {file} -acodec {codec} -ab {bitrate} {outputfile}")
            #err,out=(ffmpeg.run(stream, cmd="binary/ffmpeg.exe",capture_stdout=True, capture_stderr=True, input=None, quiet=False, overwrite_output=True))
            #print("out***********: ",out,"outerr*********: ",err)
        except ffmpeg.Error as e:
            print("err*********:" ,e.stderr, file=sys.stderr)
        # If stream is progressive

    else:
        #title=title+".mp4"
        vid.download(output_path=BaseDir, filename=title)
    #video = BaseDir + "\\.temp" + title + "\\" + title + ".mp4"
    #audio = BaseDir + "\\.temp" + "\\" + title + ".mp3"
    #output = BaseDir + "\\" + title + ".mp4"
    #OP = merge_audio_video(video, audio, output)
    #print(OP)
    file=BaseDir+"/"+title
    print("file",file)
    return render(request, 'ytdl/download.html/', {'file': file, 'title': title})

#serve over client now
def download(request):
    document_root = settings.MEDIA_ROOT
    print("Media root",document_root)
    BaseDir = BASE_DIR
    title=request.GET.get('title', 'default')
    title="COSTA"
    print("title:",title)
    file_path = BaseDir + "\\" + title+".mp4"

    print("file_path",file_path)
    #file_path = os.path.join(settings.MEDIA_ROOT, path)
    with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.rar")
            response['Content-Disposition'] = 'inline; filename=' + file_path
            return response


def download_completed(request):
    return render(request, 'ytdl/index.html')