from django.urls import path

from . import views

app_name = "library"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("books/", views.BookListView.as_view(), name="book_list"),
    path("books/create/", views.BookCreateView.as_view(), name="book_create"),
    path("books/<int:pk>/edit/", views.BookUpdateView.as_view(), name="book_update"),
    path("books/<int:pk>/delete/", views.BookDeleteView.as_view(), name="book_delete"),
    path("members/", views.MemberListView.as_view(), name="member_list"),
    path("members/create/", views.MemberCreateView.as_view(), name="member_create"),
    path("members/<int:pk>/edit/", views.MemberUpdateView.as_view(), name="member_update"),
    path("members/<int:pk>/delete/", views.MemberDeleteView.as_view(), name="member_delete"),
    path("issue/", views.issue_book, name="issue_book"),
    path("return/", views.return_book, name="return_book"),
    path("borrows/", views.borrow_list, name="borrow_list"),
    path("fines/", views.fine_list, name="fine_list"),
]
