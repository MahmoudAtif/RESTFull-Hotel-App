from django.shortcuts import render

from django.http import HttpResponse
import requests
import json



def send_notification(registration_ids , message_title , message_desc):
    fcm_api = "AAAA0hh4Oqk:APA91bGGzEjMNgPFogsMCx6r3vdOhSMWec55JZBDwqsmaenEwm7cDF2zPhN6AfT2yoPTuYaEFJUnuVPEzbikUewwOqj2S81Z4AhXlJla47Y70YczgiJuYNNVl2_GdvLv3l1jMROlBWsd"
    url = "https://fcm.googleapis.com/fcm/send"
    
    headers = {
    "Content-Type":"application/json",
    "Authorization": 'key='+fcm_api}

    payload = {
        "registration_ids" :registration_ids,
        "priority" : "high",
        "notification" : {
            "body" : message_desc,
            "title" : message_title,
            "image" : "https://i.ytimg.com/vi/m5WUPHRgdOA/hqdefault.jpg?sqp=-oaymwEXCOADEI4CSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLDwz-yjKEdwxvKjwMANGk5BedCOXQ",
            "icon": "https://yt3.ggpht.com/ytc/AKedOLSMvoy4DeAVkMSAuiuaBdIGKC7a5Ib75bKzKO3jHg=s900-c-k-c0x00ffffff-no-rj",
            
        }
    }

    result = requests.post(url,  data=json.dumps(payload), headers=headers )
    print(result.json())





def index(request):
    
    return render(request , 'index.html')

def send(request):
    resgistration  = [
        'dEq0UfztG1N_lkeRLRkir3:APA91bFJnthLymhglMiH2nHo129tRd3JF69nuWooamRvm8jFw8P5_YiH4EyPYVeCDZo28YCXhlJY4K7ITm3v0dMdcNb05LvLugkXr1-eKdrk2dyBO_50UX3amwIwdam0raNXPmlvfQiV'
    ]
    send_notification(resgistration , 'Code Keen added a new video' , 'Code Keen new video alert')
    return HttpResponse("sent")




def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js"); ' \
         'var firebaseConfig = {' \
         '        apiKey: "AIzaSyCUpDGRrkDHfF-4NaX0Km6erAuULqaAbkg",' \
         '        authDomain: "django-project-edd3c.firebaseapp.com",' \
         '        projectId: "django-project-edd3c",' \
         '        storageBucket: "django-project-edd3c.appspot.com",' \
         '        messagingSenderId: "902353664681",' \
         '        appId: "1:902353664681:web:05fbd4900e55014651c7b8",' \
         '        measurementId: "G-LNTGRKQGPW"' \
         ' };' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

    return HttpResponse(data,content_type="text/javascript")