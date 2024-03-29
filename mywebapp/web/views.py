from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django import forms
from web.models import Post, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


# create form classes                  

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter title', 'style': 'font-size: 23px; height: 50px, width:80%;'}),
            'content': forms.Textarea(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter content', 'rows': 15, 'style': 'font-size: 20px; width: 80%;'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control form-control-lg', 'placeholder': '답변 작성', 'rows': 10, 'style': 'font-size: 18px;'}),
        }
        
# rendering each page
def index(request): 
    return render(request, 'introduction.html')

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'myapp/home.html', {'posts': posts})

def post_detail(request, board, post_id):
    post = get_object_or_404(Post, id=post_id, board=board)
    return render(request, 'post_detail.html', {'post': post})

def math(request, board): # add board. debug this!!! 
    posts = Post.objects.filter(board='math')
    return render(request, 'math.html', {'posts': posts, 'contents':board}) 

def english(request, board):
    posts = Post.objects.filter(board='english')
    return render(request, 'english.html', {'posts': posts, 'contents':board})

def science(request, board):
    posts = Post.objects.filter(board='science')
    return render(request, 'science.html', {'posts': posts, 'contents':board})

def introduction(request):
    return render(request, 'introduction.html') 


# implement sign up and sign in before posting. 
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('introduction')
    else:
        form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})

def post_actions(request, action, board=None, post_id=None):
    if action == 'add_post':
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.board = board
                post.author = request.user  # Assuming user authentication is implemented
                post.save()   #post_id 는 save되면서 자동으로 생성됨. 
                return redirect(board, board=board) #여기서 에러 생김!!
        else:
            form = PostForm()
        return render(request, 'add_post.html', {'form': form, 'board': board})

    elif action == 'add_comment':
        post = get_object_or_404(Post, id=post_id)
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user  # Assuming user authentication is implemented
                comment.save()
                return redirect('post_detail',  post_id=post.id) #여기서 에러 주의!
        else:
            form = CommentForm()
        return render(request, 'add_comment.html', {'form': form, 'post': post})

    elif action == 'post_detail':
        #post = get_object_or_404(Post, id=post_id, board=board)
        post = get_object_or_404(Post, id=post_id)
        return render(request, 'post_detail.html', {'post': post}) # 여기서 에러 주의!

    else:
        return redirect('index')


# 글, 댓글 수정, 삭제 , 
@login_required
def delete_post(request, post_id, board):
    post = get_object_or_404(Post, id=post_id)
    
    if post.author != request.user:
        raise PermissionDenied
    
    if request.method == 'POST':
        post.delete()
        return redirect(board, board=board)
        
    return render(request, 'delete_post.html', {'post': post})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if post.author != request.user:
        raise PermissionDenied
    
    if request.method == 'POST':
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.save()
        return redirect('post_detail', post_id=post.id)
        
    return render(request, 'edit_post.html', {'post': post})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if comment.author != request.user:
        raise PermissionDenied
    
    if request.method == 'POST':
        comment.delete()
        return redirect('post_detail', post_id=comment.post.id)
        
    return render(request, 'delete_comment.html', {'comment': comment})

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if comment.author != request.user:
        raise PermissionDenied
    
    if request.method == 'POST':
        comment.content = request.POST['content']
        comment.save()
        return redirect('post_detail', post_id=comment.post.id)
        
    return render(request, 'edit_comment.html', {'comment': comment})

