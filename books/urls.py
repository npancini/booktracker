from django.urls import path
from books import views, api_views

urlpatterns = [
    path("", views.books_list, name="list"),
    # Friends
    path("friends/", views.friends_page, name="friends"),
    path("api/friends/", api_views.list_friends, name="list_friends"),
    path("api/friends/requests/", api_views.list_friend_requests, name="list_friend_requests"),
    path("api/friends/search/", api_views.search_users, name="search_users"),
    path("api/friends/request/send/", api_views.send_friend_request, name="send_friend_request"),
    path("api/friends/request/<int:request_id>/respond/", api_views.respond_friend_request, name="respond_friend_request"),
    path("api/friends/remove/", api_views.remove_friend, name="remove_friend"),
    path("api/friends/<str:username>/books/", api_views.friend_books, name="friend_books"),
    path("api/friends/<str:username>/books/<int:book_id>/notes/", api_views.friend_book_notes, name="friend_book_notes"),
    path('add/', api_views.add_book, name='add'),
    path('<int:pk>/', views.book_detail, name='detail'),
    path('<int:pk>/delete/', views.delete_book, name='delete'),
    path("api/books/<int:pk>/notes/", api_views.book_notes_api, name="book_notes_api"),
    path("api/books/<int:pk>/notes/add/", api_views.add_note_api, name="add_note_api"),
    path("api/notes/<int:pk>/delete/", api_views.delete_note_api),
    path("api/notes/<int:pk>/edit/", api_views.edit_note_api),
    path("api/open-library-search/", api_views.open_library_search),
    path("search/", views.book_search, name="book_search"),
    path("add-from-search/", views.add_book_from_search, name="add_book_from_search"),
    path("<int:id>/finish/", views.finish_book, name="finish_book"),
    path('reading_stats/', views.reading_stats, name='reading_stats'),
    path("<int:id>/update-date/", views.update_finish_date, name="update_finish_date"),
]