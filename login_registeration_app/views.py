from django.http import request
from music_app.models import Music, Rate
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from login_registeration_app.models import *
from django.contrib import messages
from django.db.models import Count
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
import bcrypt
from django.http import JsonResponse
# Create your views here.
def root(request):
    return redirect('/login')
def login (request):
    if 'user' not in request.session:
        return render(request,"login.html")
    return redirect('/home')
def logins(req):
    req.session.clear()
    user = User.objects.filter(username = req.POST['username'])
    psswd = req.POST['passwd'] 
    if user:
        logged_user=user[0]
        if bcrypt.checkpw(psswd.encode(), logged_user.password.encode()):
            req.session['user']={
                'fname':logged_user.first_name,
                'lname':logged_user.last_name,
                'id':logged_user.id,
                'role':logged_user.role.role,
                
            }
            context= {
                'userimg' : User.objects.get(id=req.session['user']['id']),
                'allimgs' : User.objects.all()
            }
            return render(req,'home.html',context)
        else:
            req.session['wrngpass']="password is wrong"
            return redirect('/')
    else:
        req.session['wrngemail']="email is wrong"
        return redirect('/')
def register(request):
    return render(request,'registeration.html')
def home(req):
    if 'user' in req.session:
        allmusic = Music.objects.all()
        context = {
        'allmusic':allmusic
        }
        return render(req,'home.html',context)
    return redirect('/')
def adduser(request):
    if 'user' in request.session :
        return redirect('/home')
    errors=User.objects.basic_validator(request.POST)
    if len(errors)>0:
        for key,value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        hashpassword= bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user=User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        password=hashpassword,
        email=request.POST['email'],
        username=request.POST['user_name'],
        birh_date=request.POST['birth_date'],
        gender=Gender.objects.get(id=request.POST['gender']),
        image=request.FILES['img'],
        role=Role.objects.get(id=2)
        )
        request.session['user']={
            'id':user.id,
            'fname':user.first_name,
            'lname':user.last_name,
        }
        return redirect('/home')
def artists(request):
    users= User.objects.filter(role = Role.objects.get(id = 1))
    page = request.GET.get('page', 1)
    paginator = Paginator (users, 5)

    try:
        artists = paginator.page(page)
    except PageNotAnInteger:
        artists = paginator.page(1)
    except EmptyPage:
        artists= paginator.page(paginator.num_pages)
    context = {
        'all_artists':users,
        'artists' : artists
    
    }
    return render(request,'artistspage.html', context)

def userprofile(req):
    user = User.objects.get(id=req.session['user']['id'])
    allmusic = Music.objects.filter(uploaded_by=user)
    followings=user.userfollowings.all()
    ratings=user.rates.all()
    queryset=LOL.objects.filter(user=user)
    if  queryset.exists():
        typex=1
    else:
        typex=2
    context={
        'x': user,
        'allmusic':allmusic,
        'type':typex,
        'followings':followings,
        'ratings':ratings
    }
    if user.role == Role.objects.get(id=2):
        return render(req,'userprofile.html',context)
    return render(req,'artistpage.html',context)
def artistprofile(req,id):
    followed_user=User.objects.get(id=id)
    followers = Follower.objects.filter(followeduser=followed_user).count()
    user = User.objects.get(id=id)
    me = User.objects.get(id = req.session['user']['id'])
    allmusic = Music.objects.filter(uploaded_by=user)
    g=0
    for i in user.userfollowers.all():
        if me.id == i.followinguser.id :
            g=g+1
    context = {
        'x': user,
        'allmusic':allmusic,
        'me':me,
        'g':g,
        'number_of_followers': followers 
        
    }
    return render(req,'artistPage.html',context)
def addmusic(req,id):
    user = User.objects.get(id = id)
    song_title = req.POST['songtitle']
    song_writer  = req.POST['songwriter']
    song_composer = req.POST['songcomposer']
    mp3file = req.FILES['songmp3']
    duration = 3
    Music.objects.create(song_name = song_title , writer = song_writer ,composer = song_composer , duration = duration , music = mp3file , uploaded_by = user  )
    return redirect('/artistprofile/'+str(id))
sum1=0
sum2=0
def songpage(req,id):
    global sum1,sum2
    z = Music.objects.get(id=id)
    print(z.song_name)
    user=User.objects.get(id=req.session['user']['id'])
    Ratingusers=z.rates.count()
    for i in z.rates.all():
        sum1=sum1+i.score
        sum2=sum2+1
    rate=int(sum1/sum2)
    num=rate
    if rate == 1:
        rate="first"
    elif rate == 2:
        rate="second"
    elif rate == 3:
        rate="third"
    elif rate == 4 :
        rate="fourth"
    elif rate== 5:
        rate = "fifth"
    context = {
        'filter':user.rates.filter(music=z),
        'i':z,
        'rate':rate,
        'user':user,
        'num':num,
        'users':Ratingusers
        }
    return render(req,'songpage.html',context)
def logout(req):
    req.session.clear()
    return redirect('/')
def delete(req,id):
    song = Music.objects.get(id=id)
    song.delete()
    return redirect('/artistprofile/'+str(req.session['user']['id']))
def requesttobeartist(req):
    user = User.objects.get(id = req.session['user']['id'])
    LOL.objects.create(user=user,bool=True)
    return redirect('/userprofile')
    

def admin(req):
    role=Role.objects.get(id=2)
    userrole=Role.objects.get(id=1)
    if 'user' in req.session:
        if 'role' in req.session['user']:
            if req.session['user']['role']=="admin":
                context= {
                                'user' : User.objects.get(id=req.session['user']['id']),
                                'user' : User.objects.get(id=req.session['user']['id']),
                                'music_count':Music.objects.count(),
                                'user_count':User.objects.filter(role=userrole).count(),
                                'artist_count':User.objects.filter(role=role).count(),
                            }
                return render(req,'welcomeadmin.html',context)
            else:
                return redirect('/home')
    else:
        return render(req,"adminlogin.html")
def adminhandle(req):
    if req.method == "GET":
        return redirect('/admin')
    if req.method == "POST":
        user = User.objects.filter(username = req.POST['user'])
        psswd = req.POST['pass'] 
        role=Role.objects.get(id=2)
        userrole=Role.objects.get(id=1)
        if user:
            logged_user=user[0]
            if logged_user.role.role=="admin":
                if bcrypt.checkpw(psswd.encode(), logged_user.password.encode()):
                    req.session['user']={
                        'fname':logged_user.first_name,
                        'lname':logged_user.last_name,
                        'id':logged_user.id,
                        'role':logged_user.role.role,
                        
                    }
                    context= {
                        'user' : User.objects.get(id=req.session['user']['id']),
                        'music_count':Music.objects.count(),
                        'user_count':User.objects.filter(role=userrole).count(),
                        'artist_count':User.objects.filter(role=role).count(),
                        
                    }
                return render(req,'welcomeadmin.html',context)
            return redirect('/admin')
    else:
        return('/home')
def adminprofile(req):
    if req.session['user']['role'] != 'admin':
        return redirect('/home')
    user=User.objects.get(id=req.session['user']['id'])
    context={
        'user':user
    }
    return render(req,"adminprofile.html",context)
def artistrequest(req):
    if req.session['user']['role'] != 'admin':
        return redirect('/home')
    user=User.objects.get(id=req.session['user']['id'])
    if user.role.role == "admin":
        all=LOL.objects.all()
        context={
            'all':all,
            'user':user
        }
    return render(req,"artistrequest.html",context)
def acceptartist(req,id):
    if req.session['user']['role'] != 'admin':
        return redirect('/home')
    user=User.objects.get(id=id)
    user.role=Role.objects.get(id=1)
    user.save()
    lol=LOL.objects.get(user=user)
    lol.delete()
    return redirect('/admin')

def declineartist(req,id):
    if req.session['user']['role'] != 'admin':
        return redirect('/home')
    user=User.objects.get(id=id)
    lol=LOL.objects.get(user=user)
    lol.delete()
    return redirect('/artistrequest')

def allusers(req):
    if req.session['user']['role'] != 'admin':
        return redirect('/home')
    user=User.objects.get(id=req.session['user']['id'])
    all=User.objects.all()
    allroles=Role.objects.all()
    context={
        'all':all,
        'user':user,
        'allroles':allroles
    }
    return render(req,"allusers.html",context)
def allmusic(req):
    if req.session['user']['role'] != 'admin':
        return redirect('/home')
    user=User.objects.get(id=req.session['user']['id'])
    all=Music.objects.all()
    context={
        'user':user,
        'all':all,
    }
    return render(req,"allmusic.html",context)
def deleteuser(req,id):
    if req.session['user']['role'] != 'admin':
        return redirect('/home')
    user=User.objects.get(id=id)
    user.delete()
    return redirect('/adminallusers')
def deletemusic(req,id):
    if req.session['user']['role'] != 'admin':
        return redirect('/home')
    music=Music.objects.get(id=id)
    music.delete()
    return redirect('/allmusic')
def update(request,id):
    if request.session['user']['role'] != 'admin':
        return redirect('/home')
    role=Role.objects.get(id=request.POST['role'])
    user=User.objects.get(id=id)
    user.first_name=request.POST['fname']
    user.last_name=request.POST['lname']
    user.username=request.POST['username']
    user.role=role
    user.save()
    return redirect('/adminallusers')
def follow(request,id):
    user=User.objects.get(id=id)
    folower=User.objects.get(id=request.session['user']['id'])
    Follower.objects.create(followeduser=user,followinguser=folower)
    return redirect('/artistprofile/'+str(id))

def unfollow(request,id):
    user=User.objects.get(id=id)
    folower=User.objects.get(id=request.session['user']['id'])
    x=Follower.objects.get(followeduser=user,followinguser=folower)
    x.delete()
    return redirect('/artistprofile/'+str(id))
def release(request):
    context={
        'allmusic':Music.objects.order_by('-created_at').all()[:10],
        'msg':"Newest Releases"
    }
    return render (request,"release.html",context)

def top10(request):
    context={
        'allmusic':Music.objects.all()[:10],
        'msg':"Top 10 Music"
    }
    return render (request,"release.html",context)
def autocomplete(request, str):
    data={}
    x=User.objects.filter(first_name__contains=str)
    names=[]
    for i in x:
        names.append(i.first_name)
    
    data['names'] = names
    return JsonResponse(data)



def lol(request):
    if request.method == "POST":
        searched = request.POST['txtSearch']
        value_to_search = User.objects.filter(first_name = searched)
        user=value_to_search[0]
        id=user.id
        return redirect('artistprofile/'+str(id))
def rate_image(request,id):
    user=User.objects.get(id=request.session['user']['id'])
    music=Music.objects.get(id=id)
    if 'first' in request.POST:
        Rate.objects.create(music=music,user=user,score=1)
    if 'second' in request.POST:
        Rate.objects.create(music=music,user=user,score=2)
    if 'third' in request.POST:
        Rate.objects.create(music=music,user=user,score=3)
    if 'fourth' in request.POST:
        Rate.objects.create(music=music,user=user,score=4)
    if 'fifth' in request.POST:
        Rate.objects.create(music=music,user=user,score=5)
    return redirect('/songpage/'+str(id))