from ..views import (
    ManagementView, ManagementProductView, ManagementProductsView, ManagementAddProductView,
    ManagementCategoriesView, ManagementCategoryView, ManagementAddCategoryView, ManagementDeleteCategoryView,
    ManagementUsersView, ManagementReviewsView,
)

urls = [
    # Админка
    ("management:management", ManagementView, "???", 200),
    ("management:management-products", ManagementProductsView, "???", 200),
    ("management:management-add-product", ManagementAddProductView, "???", 200),
    ("management:management-product", ManagementProductView, {'slug': 'unmalted-wheat'}, 200),
    ("management:management-categories", ManagementCategoriesView, "???", 200),
    ("management:management-add-category", ManagementAddCategoryView, "???", 200),
    ("management:management-category", ManagementCategoryView, {'slug': 'yeast'}, 200),
    ("management:management-delete-category", ManagementDeleteCategoryView, {'pk': 1}, 200),
    ("management:management-users", ManagementUsersView, "???", 200),
    ("management:management-reviews", ManagementReviewsView, "???", 200),
]