from django.contrib import admin

from .models import Book, Borrow, Fine, Member


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "isbn", "total_copies", "available_copies")
    search_fields = ("title", "author", "isbn")
    readonly_fields = ("total_copies",)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone", "joined_at")
    search_fields = ("full_name", "email", "phone")
    list_filter = ("joined_at",)


@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ("member", "book", "borrow_date", "due_date", "return_date")
    search_fields = ("member__full_name", "book__title")
    list_filter = ("borrow_date", "due_date", "return_date")


@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    list_display = ("borrow", "days_late", "amount", "created_at")
    search_fields = ("borrow__member__full_name", "borrow__book__title")

# Register your models here.
