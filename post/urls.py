from django.urls import path,include
from .views import PostList,Postcreate,PostDetail,PostUpdate,PostDelete,commentcreate,commentDetails,commentList,PostLike

app_name = 'posts'
urlpatterns = [
    path('',PostList.as_view(),name="post-list"),
    path('post/create/',Postcreate.as_view(),name="post-create"),
    path('post/<int:pk>/details/',PostDetail.as_view(),name="post-details"),
    path('post/<int:pk>/update/',PostUpdate.as_view(),name="post-update"),
    path('post/<int:pk>/delete/',PostDelete.as_view(),name="post-delete"),
    path('post/<int:pk>/like/',PostLike.as_view(),name="post-like"),
    path('comment/',commentList.as_view(),name="comment-list"),
    path('comment/<int:pk>/',commentDetails.as_view(),name="comment-details"),
    path('comment/<int:pk>/create/',commentcreate.as_view(),name="Comment-create"),
    
]