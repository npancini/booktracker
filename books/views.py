from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models.functions import ExtractMonth
from datetime import datetime
from .models import Book
from django.db.models import Count
import requests


app_name = 'books'

@login_required
def friends_page(request):
    return render(request, 'books/friends.html')


@login_required
def books_list(request):
    status = request.GET.get("status", "all")

    books = Book.objects.filter(user=request.user)

    if status == "finished":
        books = books.filter(finished=True)

    elif status == "reading":
        books = books.filter(finished=False)

    context = {
        "books": books,
        "status": status,
    }

    return render(request, "books/books_list.html", context)

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)
    return render(request, 'books/book_detail.html', {'book': book})

def finish_book(request, id):
    book = get_object_or_404(Book, id=id, user=request.user)

    if request.method == "POST":
        book.finished = True
        book.finish_date = timezone.now().date()
        book.save()

    return redirect("books:detail", pk=book.id)

def update_finish_date(request, id):
    book = get_object_or_404(Book, id=id, user=request.user)

    if request.method == "POST":
        new_date = request.POST.get("finish_date")

        if new_date:
            book.finish_date = new_date
            book.save()

    return redirect("books:detail", pk=book.id)

@require_POST
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)
    book.delete()
    return redirect('books:list')

def book_search(request):
    query = request.GET.get("q")
    page = request.GET.get("page", 1)

    results = []
    num_found = 0

    if query:
        url = "https://openlibrary.org/search.json"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            url,
            params={
                "q": query,
                "page": page
            },
            headers=headers
        )

        try:
            data = response.json()
        except ValueError:
            data = {}
        results = []
        num_found = data.get("numFound", 0)

        for book in data.get("docs", []):
            cover_id = book.get("cover_i")

            cover_url = None
            if cover_id:
                cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"

            results.append({
                "title": book.get("title"),
                "author": book.get("author_name", ["Unknown"])[0],
                "cover_url": cover_url,
            })

    return render(request, "books/search_results.html", {
        "results": results,
        "query": query,
        "page": int(page),
        "num_found": num_found,
    })

@login_required
def add_book_from_search(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        cover_url = request.POST.get("cover_url")

        Book.objects.create(
            user=request.user,
            title=title,
            author=author,
            cover_url=cover_url or None
        )

    return redirect("books:list")

def reading_stats(request):

    current_year = timezone.now().year

    selected_year = request.GET.get("year")

    if selected_year:
        selected_year = int(selected_year)
    else:
        selected_year = current_year

    books = Book.objects.filter(
        user=request.user,
        finished=True,
        finish_date__year=selected_year
    )

    total_books = books.count()

    monthly_data = (
        books
        .annotate(month=ExtractMonth("finish_date"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    monthly_counts = [0] * 12

    for item in monthly_data:
        monthly_counts[item["month"] - 1] = item["count"]

    years = range(current_year, current_year - 50, -1)

    context = {
        "selected_year": selected_year,
        "years": years,
        "total_books": total_books,
        "monthly_counts": monthly_counts,
    }

    return render(request, "books/reading_stats.html", context)