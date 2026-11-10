from django.shortcuts import render


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