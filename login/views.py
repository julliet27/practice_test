from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import UserSerializer, BookSerializer, BorrowingSerializer
from .models import User, Book, Borrowing

class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookManagement(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_admin:
            return Response({'error': 'Only admins can add books.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BorrowBook(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        book_id = request.data.get('book_id')
        book = Book.objects.filter(id=book_id).first()
        if not book or book.available_copies <= 0:
            return Response({'error': 'Book is not available.'}, status=status.HTTP_400_BAD_REQUEST)

        borrowing = Borrowing.objects.create(user=request.user, book=book)
        book.available_copies -= 1
        book.save()
        return Response(BorrowingSerializer(borrowing).data, status=status.HTTP_201_CREATED)

class ReturnBook(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, borrowing_id):
        borrowing = Borrowing.objects.filter(id=borrowing_id, user=request.user).first()
        if not borrowing or borrowing.returned:
            return Response({'error': 'Invalid return request.'}, status=status.HTTP_400_BAD_REQUEST)

        borrowing.returned = True
        borrowing.save()
        borrowing.book.available_copies += 1
        borrowing.book.save()
        return Response({'message': 'Book returned successfully.', 'fine': borrowing.calculate_fine()})
