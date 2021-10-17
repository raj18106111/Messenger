from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Friend

# Create your views here.
def home(request):
    if request.user.is_anonymous or request.user.is_active==False:
        return redirect('/accounts/login')
    return render(request, 'home.html')

def checkview(request):
    if request.user.is_anonymous or request.user.is_active==False:
        return redirect('/accounts/login')
    if request.method == 'POST':
        friendusername = request.POST.get("friendusername")
        request.session['friend'] = friendusername
        if request.user.username==friendusername:
            return redirect('/')
        current_user = request.user.username
        roomname = "".join(sorted(current_user+friendusername))
        if User.objects.filter(username=friendusername).exists():
            return redirect('/room/'+roomname)
        else:
            return redirect('/')
    
    return redirect('/')

num = 0
def room(request,roomname):                                                                                                               
    if request.user.is_anonymous or request.user.is_active==False:
        return redirect('/accounts/login')
    current_user = request.user.username
    friend = request.session.get('friend')
    if current_user == roomname:
        return redirect('/')
    global num
    num += 1
    return render(request, 'room.html',{'friend':friend,'roomname':roomname,'user':current_user,'count':num})


def friends(request):
    if request.user.is_anonymous or request.user.is_active==False:
        return redirect('/accounts/login')
    if request.method=='POST':
        friend=request.POST.get('friendusername')
        nickname=request.POST.get('friendnickname')
        user=request.user.username
        if friend==user:
            return redirect('/friends')
        if friend=="" or nickname=="":
            return redirect('/friends')
        if Friend.objects.filter(friend=friend).filter(user=user).exists():
            return redirect('/friends')
        if User.objects.filter(username=friend).exists()==False:
            return redirect('/friends')
        new_friend=Friend.objects.create(user=user, nickname=nickname,friend=friend)
        new_friend.save()
    
    unsorted_friends=Friend.objects.all().filter(user=request.user.username)
    user_friends=sorted(list(unsorted_friends.values()),key=lambda k:k['nickname'].lower())
    return render(request,'friends.html',{"user_friends": user_friends})


def removefriend(request):
    if request.user.is_anonymous or request.user.is_active==False:
        return redirect('/accounts/login')
    
    if request.method =='POST':
        friend=request.POST.get('friendusername')
        user=request.user.username
        if Friend.objects.all().filter(friend=friend).filter(user=user).exists()==False:
            return redirect('/friends')

        remove_friend=Friend.objects.all().filter(friend=friend).filter(user=user)
        remove_friend[0].delete()
        return redirect('/friends')

    return redirect('/friends')

