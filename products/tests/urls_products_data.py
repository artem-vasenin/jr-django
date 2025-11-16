from ..views import DetailsView, GuidesView, HomeView, AddReviewView

urls = [
    # Админка
    ("products:home", HomeView, "???", 200),
    ("products:guides", GuidesView, "???", 200),
    ("products:add-review", AddReviewView, "???", 200),
    ("products:product", DetailsView, {'slug': 'unmalted-wheat'}, 200),
]