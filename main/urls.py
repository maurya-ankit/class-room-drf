from django.urls import path,include
from . import views



urlpatterns = [
    path("",views.UserList.as_view(),name="user-list"),
    # path('', include(router.urls)),
    path("<int:pk>/",views.UserDetail.as_view(),name="user-detail"),
    path("posts/",views.ClassroomPostList.as_view(),name="posts-list"),
    path("posts/<int:pk>",views.ClassroomPostDetail.as_view(),name="posts-detail"),
    path("posts/comments/",views.ClassroomPostCommentList.as_view(),name="comment-list"),
    path("posts/comments/<int:pk>",views.ClassroomPostCommentDetail.as_view(),name="comment-detail"),
    path("classroom/",views.ClassroomList.as_view(),name="classroom-list"),
    path("classroom/<int:pk>",views.ClassroomDetail.as_view(),name="classroom-detail"),
    path("membership/",views.MembershipList.as_view(),name="membership-list"),
    path("membership/<int:pk>",views.MembershipDetail.as_view(),name="membership-detail"),

]