from django.shortcuts import render
from datetime import datetime


def home_view(request):
    # Datos simulados
    videos = [
        {
            "title": "Video 1",
            "embed_url": "https://www.youtube.com/embed/R-pNoy2GgPQ?si=2l_R3LL7sXiOMMrQ",
            "username": "user1",
            "date_post": datetime(2023, 10, 1),
        },
        {
            "title": "Video 2",
            "embed_url": "https://www.youtube.com/embed/3JZ_D3ELwOQ",
            "username": "user2",
            "date_post": datetime(2023, 10, 2),
        },
        {
            "title": "Video 3",
            "embed_url": "https://www.youtube.com/embed/tgbNymZ7vqY",
            "username": "user3",
            "date_post": datetime(2023, 10, 3),
        },
    ]
    return render(
        request, "pages/home.html", {"videos": videos}
    )
