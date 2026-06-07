from django.http import JsonResponse
from .models import Book, Note
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import get_object_or_404
import requests

@login_required
def add_book(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            title = data.get("title")
            author = data.get("author")

            if not title or not author:
                return JsonResponse(
                    {"error": "Missing required fields"},
                    status=400
                )

            book = Book.objects.create(
                title=title,
                author=author,
                user=request.user
            )

            return JsonResponse({
                "id": book.id,
                "title": book.title,
                "author": book.author,
            }, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def book_notes_api(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)

    notes = list(
        Note.objects.filter(book=book)
        .values("id", "content", "page_number", "chapter", "created_at")
        .order_by("-created_at")
    )

    return JsonResponse(notes, safe=False)

@login_required
@require_POST
def add_note_api(request, pk):
    try:
        book = get_object_or_404(Book, pk=pk, user=request.user)
        data = json.loads(request.body)

        content = data.get("content")
        page_number = data.get("page_number")
        chapter = data.get("chapter")

        if not content:
            return JsonResponse(
                {"error": "Content is required"},
                status=400
            )

        note = Note.objects.create(
            book=book,
            content=content,
            page_number=page_number or None,
            chapter=chapter or None,
        )

        return JsonResponse({
            "id": note.id,
            "content": note.content,
            "page_number": note.page_number,
            "chapter": note.chapter,
            "created_at": note.created_at,
        }, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@login_required
@require_POST
def delete_note_api(request, pk):
    note = get_object_or_404(Note, pk=pk, book__user=request.user)
    note.delete()
    return JsonResponse({"success": True})

@login_required
@require_POST
def edit_note_api(request, pk):
    note = get_object_or_404(Note, pk=pk, book__user=request.user)

    data = json.loads(request.body)
    content = data.get("content")
    page_number = data.get("page_number")
    chapter = data.get("chapter")

    if not content:
        return JsonResponse({"error": "Content is required"}, status=400)

    note.content = content
    note.page_number = page_number or None
    note.chapter = chapter or None
    note.save()

    return JsonResponse({
        "id": note.id,
        "content": note.content,
        "page_number": note.page_number,
        "chapter": note.chapter,
    })

@login_required
@require_GET
def open_library_search(request):
    query = request.GET.get("q")

    if not query:
        return JsonResponse({"error": "No query provided"}, status=400)

    url = "https://openlibrary.org/search.json"

    response = requests.get(url, params={"q": query})

    if response.status_code != 200:
        return JsonResponse({"error": "Open Library error"}, status=500)

    data = response.json()

    # Return only what we care about
    results = []

    for book in data.get("docs", [])[:10]:
        results.append({
            "title": book.get("title"),
            "author": book.get("author_name", ["Unknown"])[0],
            "first_publish_year": book.get("first_publish_year"),
        })

    return JsonResponse({"results": results})

# ─── Friends API ────────────────────────────────────────────────────────────

from .models import FriendRequest
from django.contrib.auth.models import User
from django.db.models import Q


def get_friends(user):
    """Return queryset of Users who are accepted friends of user."""
    accepted = FriendRequest.objects.filter(
        Q(from_user=user, accepted=True) | Q(to_user=user, accepted=True)
    )
    friend_ids = []
    for req in accepted:
        if req.from_user == user:
            friend_ids.append(req.to_user_id)
        else:
            friend_ids.append(req.from_user_id)
    return User.objects.filter(id__in=friend_ids)


def are_friends(user_a, user_b):
    return FriendRequest.objects.filter(
        Q(from_user=user_a, to_user=user_b, accepted=True) |
        Q(from_user=user_b, to_user=user_a, accepted=True)
    ).exists()


@login_required
def search_users(request):
    """GET /api/friends/search/?q=username"""
    q = request.GET.get('q', '').strip()
    if not q:
        return JsonResponse({'results': []})

    users = User.objects.filter(username__icontains=q).exclude(id=request.user.id)[:10]
    friends = get_friends(request.user)
    friend_ids = set(friends.values_list('id', flat=True))

    # pending requests sent by me
    pending_sent = set(
        FriendRequest.objects.filter(from_user=request.user, accepted=False)
        .values_list('to_user_id', flat=True)
    )
    # pending requests sent to me
    pending_received = set(
        FriendRequest.objects.filter(to_user=request.user, accepted=False)
        .values_list('from_user_id', flat=True)
    )

    results = []
    for u in users:
        if u.id in friend_ids:
            status = 'friend'
        elif u.id in pending_sent:
            status = 'pending_sent'
        elif u.id in pending_received:
            status = 'pending_received'
        else:
            status = 'none'
        results.append({'id': u.id, 'username': u.username, 'status': status})

    return JsonResponse({'results': results})


@login_required
@require_POST
def send_friend_request(request):
    """POST /api/friends/request/send/  body: {to_user_id: int}"""
    data = json.loads(request.body)
    to_id = data.get('to_user_id')
    if not to_id:
        return JsonResponse({'error': 'to_user_id required'}, status=400)

    to_user = get_object_or_404(User, id=to_id)

    if to_user == request.user:
        return JsonResponse({'error': 'Cannot friend yourself'}, status=400)

    if are_friends(request.user, to_user):
        return JsonResponse({'error': 'Already friends'}, status=400)

    obj, created = FriendRequest.objects.get_or_create(
        from_user=request.user, to_user=to_user
    )
    if not created:
        return JsonResponse({'error': 'Request already sent'}, status=400)

    return JsonResponse({'success': True, 'request_id': obj.id}, status=201)


@login_required
@require_POST
def respond_friend_request(request, request_id):
    """POST /api/friends/request/<id>/respond/  body: {accept: true/false}"""
    freq = get_object_or_404(FriendRequest, id=request_id, to_user=request.user, accepted=False)
    data = json.loads(request.body)
    accept = data.get('accept', False)

    if accept:
        freq.accepted = True
        freq.save()
        return JsonResponse({'success': True, 'status': 'accepted'})
    else:
        freq.delete()
        return JsonResponse({'success': True, 'status': 'declined'})


@login_required
def list_friends(request):
    """GET /api/friends/"""
    friends = get_friends(request.user)
    data = [{'id': u.id, 'username': u.username} for u in friends]
    return JsonResponse({'friends': data})


@login_required
def list_friend_requests(request):
    """GET /api/friends/requests/ — incoming pending requests"""
    incoming = FriendRequest.objects.filter(to_user=request.user, accepted=False).select_related('from_user')
    data = [{'id': r.id, 'from_user': r.from_user.username, 'from_user_id': r.from_user.id} for r in incoming]
    return JsonResponse({'requests': data})


@login_required
def friend_books(request, username):
    """GET /api/friends/<username>/books/"""
    friend = get_object_or_404(User, username=username)
    if not are_friends(request.user, friend):
        return JsonResponse({'error': 'Not friends'}, status=403)

    books = Book.objects.filter(user=friend).values(
        'id', 'title', 'author', 'finished', 'finish_date', 'cover_url', 'created_at'
    )
    return JsonResponse({'books': list(books), 'username': username})


@login_required
def friend_book_notes(request, username, book_id):
    """GET /api/friends/<username>/books/<book_id>/notes/"""
    friend = get_object_or_404(User, username=username)
    if not are_friends(request.user, friend):
        return JsonResponse({'error': 'Not friends'}, status=403)

    book = get_object_or_404(Book, id=book_id, user=friend)
    notes = list(
        book.notes.values('id', 'content', 'page_number', 'chapter', 'created_at')
        .order_by('-created_at')
    )
    return JsonResponse({'notes': notes, 'book_title': book.title})


@login_required
@require_POST
def remove_friend(request):
    """POST /api/friends/remove/  body: {user_id: int}"""
    data = json.loads(request.body)
    user_id = data.get('user_id')
    other = get_object_or_404(User, id=user_id)
    FriendRequest.objects.filter(
        Q(from_user=request.user, to_user=other) |
        Q(from_user=other, to_user=request.user)
    ).delete()
    return JsonResponse({'success': True})
