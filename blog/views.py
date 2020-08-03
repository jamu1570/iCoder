from django.shortcuts import render,HttpResponse,redirect
from .models import Post,BlogComment
from django.contrib import messages


# Create your views here.

def blogHome(request):
    allpost = Post.objects.all()
    posts = {'allpost':allpost}
    return render(request,'blog/blogHome.html',posts)

def blogPost(request,slug):
    post = Post.objects.filter(slug=slug).first()
    post.views = post.views + 1
    post.save()
    comments = BlogComment.objects.filter(post=post,parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    context = {'post':post,'comments':comments,'user':request.user,'replyDict':replyDict}
    return render(request,'blog/blogPost.html',context)

def postComment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get("parentSno")
        if parentSno == "":
            comments = BlogComment(comment=comment,user=user,post=post)
            comments.save()
            messages.success(request,'your comment has been successfully posted !!')
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comments = BlogComment(comment=comment,user=user,post=post,parent=parent)   
            comments.save()
            messages.success(request,'your reply has been successfully posted !!')
    return redirect(f"/blog/{post.slug}")