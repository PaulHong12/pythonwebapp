from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # 메인 메뉴
    path('', views.index, name='index'), #website/board   
    path('introduction/', views.introduction, name='introduction'),
    path('math/', views.math, {'board': 'math'}, name='math'),
    path('english/', views.english, {'board': 'english'}, name='english'),
    path('science/', views.science, {'board': 'science'}, name='science'), 
    path('math/board/', views.post_actions, {'board': 'math'}, name='board'),  

    #글올리기 페이지
    path('math/add_post/', views.post_actions, {'board':'math','action':'add_post'}, name='add_math_post'),
    path('english/add_post/', views.post_actions, {'board': 'english','action':'add_post'}, name='add_english_post'),
    path('science/add_post/', views.post_actions, {'board':'science','action':'add_post'}, name='add_science_post'),

    #댓글달기와 포스트 디테일 페이지
    path('post/<int:post_id>/', views.post_actions, {'action':'post_detail'}, name='post_detail'), #여기서 에러
    path('post/<int:post_id>/add_comment/', views.post_actions,{'action':'add_comment'}, name='add_comment'), #이것도 디버그
    path('math/post_detail/<int:post_id>/add_comment/', views.post_actions, name='add_math_comment'),
    path('english/post_detail/<int:post_id>/add_comment/', views.post_actions, name='add_english_comment'),
    path('science/post_detail/<int:post_id>/add_comment/', views.post_actions, name='add_science_comment'),

    #로그인, 회원가입, 로그아웃 페이지
    path('signup/', views.register, name='signup'),
    path('signin/', views.user_login, name='signin'),
    path('logout/', auth_views.LogoutView.as_view(next_page='introduction'), name='logout'),


    # 글, 댓글 수정, 삭제
    path('posts/<int:post_id><str:board>/delete/', views.delete_post, name='delete_post'),
    path('posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('comments/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),

]