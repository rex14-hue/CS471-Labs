from django.shortcuts import render
from .models import Book, Student
from django.db.models import Avg, Count, Max, Min, Q, Sum

def index(request):
    return render(request, "bookmodule/index.html")


def list_books(request):
    return render(request, "bookmodule/list_books.html")


def viewbook(request, bookId):
    return render(request, "bookmodule/one_book.html")


def aboutus(request):
    return render(request, "bookmodule/aboutus.html")

def __getBooksList():
    book1 = {
        'id': 12344321,
        'title': 'Continuous Delivery',
        'author': 'J.Humble and D. Farley',
    }
    book2 = {
        'id': 56788765,
        'title': 'Reversing: Secrets of Reverse Engineering',
        'author': 'E. Eilam',
    }
    book3 = {
        'id': 43211234,
        'title': 'The Hundred-Page Machine Learning Book',
        'author': 'Andriy Burkov',
    }
    return [book1, book2, book3]


def search(request):
    if request.method == "POST":
        keyword = request.POST.get('keyword', '').strip().lower()
        is_title = request.POST.get('option1')
        is_author = request.POST.get('option2')

        results = []

        for book in __getBooksList():
            title_matches = is_title and keyword in book['title'].lower()
            author_matches = is_author and keyword in book['author'].lower()

            if title_matches or author_matches:
                results.append(book)

        return render(
            request,
            "bookmodule/bookList.html",
            {'books': results},
        )

    return render(request, "bookmodule/search.html")

def simple_query(request):
    books = Book.objects.filter(title__icontains="and")
    return render(request, "bookmodule/query_results.html", {"books": books})

def complex_query(request):
    books = (
        Book.objects.filter(
            author__isnull=False,
            title__icontains="and",
            edition__gte=2,
        )
        .exclude(price__lte=100)
        .order_by("id")[:10]
    )

    if books:
        return render(request, "bookmodule/query_results.html", {"books": books})

    return render(request, "bookmodule/index.html")

def lab8_task1(request):
    books = Book.objects.filter(Q(price__lte=80))
    return render(request, "bookmodule/query_results.html", {"books": books})

def lab8_task2(request):
    books = Book.objects.filter(
        Q(edition__gt=3) & (Q(title__icontains="qu") | Q(author__icontains="qu"))
    )
    return render(request, "bookmodule/query_results.html", {"books": books})

def lab8_task3(request):
    books = Book.objects.filter(
        ~Q(edition__gt=3)
        & (~Q(title__icontains="qu") | ~Q(author__icontains="qu"))
    )
    return render(request, "bookmodule/query_results.html", {"books": books})

def lab8_task4(request):
    books = Book.objects.order_by("title")
    return render(request, "bookmodule/query_results.html", {"books": books})

def lab8_task5(request):
    stats = Book.objects.aggregate(
        book_count=Count("id"),
        total_price=Sum("price"),
        average_price=Avg("price"),
        max_price=Max("price"),
        min_price=Min("price"),
    )
    return render(request, "bookmodule/book_stats.html", {"stats": stats})

def lab8_task7(request):
    cities = (
        Student.objects.values("address__city")
        .annotate(student_count=Count("id"))
        .order_by("address__city")
    )
    return render(request, "bookmodule/students_by_city.html", {"cities": cities})