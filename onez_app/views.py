from django.shortcuts import render,redirect
import instaloader
import os
from PIL import Image
from PIL import ImageFilter
from io import BytesIO
import base64
from pytube import YouTube
import pafy 
from bs4 import BeautifulSoup as bs
import requests
from django.conf import settings
from instascrape import Reel

def image_to_base64(image):
    buff = BytesIO()
    image.save(buff, format="PNG")
    img_str = base64.b64encode(buff.getvalue())
    img_str = img_str.decode("utf-8")  # convert to str and cut b'' chars
    return img_str


def home(request):
    return render(request, "home.html")


def HD_DP(request):
    if request.method=="POST":
        mod = instaloader.Instaloader()
        try:

            mod.login('dunver123', 'dunver@123') 
            user = request.POST.get("insta_id")
            mod.download_profile(user, profile_pic_only = True)

            folder_dir = f"{user}"
            for image in os.listdir(folder_dir):
            
                # check if the image ends with png
                if (image.endswith(".jpg")):
                    # Open an already existing image
                    imageObject = Image.open(f"{user}/{image}")

                # Apply sharp filter
                sharpened1 = imageObject.filter(ImageFilter.SHARPEN)
                sharpened2 = imageObject.filter(ImageFilter.SHARPEN)
                img = image_to_base64(imageObject)
                img1 = image_to_base64(sharpened1)
                img2 = image_to_base64(sharpened2)

                for file in os.listdir(user):
                    os.remove(f"{user}/{file}")
                os.rmdir(user)
                break
                return render(request,"hd_dp.html", {"img":img, "img1": img1, "img2":img2})
        except Exception as e:
            print(e)
            return render(request, "error.html", {"msg": "Please enter a valid username"})

    return render(request,"hd_dp.html")


def youtube_to_audio(request):

    path = settings.MEDIA_ROOT

    if request.method=="POST":
        for file in os.listdir(path+'/audio/'):
            os.remove(f"{path}/audio/{file}")
            
        yt_link = request.POST.get("yt_link")
        yt = YouTube(yt_link)
        audio = yt.streams.filter(only_audio=True)[0]
        out_file = audio.download(path)
        base, ext = os.path.splitext(out_file)
        new_file = path+'/audio/'+'youtube_audio' + '.mp3'
        os.rename(out_file,new_file)
        audio_files = os.listdir(path+'/audio/')
        return render(request, "yt_to_mp3.html", {'audio_file':audio_files})


def youtube_to_video(request):

    path = settings.MEDIA_ROOT

    if request.method=="POST":
        for file in os.listdir(path+'/video/'):
            os.remove(f"{path}/video/{file}")
            
        yt_link = request.POST.get("yt_link")
        yt = YouTube(yt_link)
        d_video = yt.streams.get_highest_resolution()
        out_file = d_video.download(path)
        base, ext = os.path.splitext(out_file)
        new_file = path+'/video/'+'youtube_video' + '.mp4'
        os.rename(out_file,new_file)
        video_file = os.listdir(path+'/video/')
        return render(request, "yt_to_mp4.html", {'video_file':video_file})


def insta_reel(request):
    path = settings.MEDIA_ROOT
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 \
        Safari/537.36 Edg/79.0.309.43",
    }
    if request.method=="POST":
        reel_link = request.POST.get("reel_link")
        insta_reel = Reel(reel_link)
        print(type(reel_link))
        insta_reel.scrape()
        insta_reel.download(fp=f"{path}/reel/insta-reel.mp4")
    return render(request, "insta_reel.html")