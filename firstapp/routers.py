from django.urls import path

from .views import MessagesView, TicketsView

urlpatterns = [
    path('tickets/', TicketsView.as_view({'get': 'list', 'post': 'create'}), name='tickets-list'),
    path('tickets/<int:id>/', TicketsView.as_view({'get': 'retrieve',
                                                   'put': 'update',
                                                   'delete': 'destroy'}), name='tickets-detail'),
    path('tickets/<int:id>/messages/', MessagesView.as_view({'get': 'list', 'post': 'create'}), name='messages-list'),
    path('tickets/<int:id>/messages/<int:pk>', MessagesView.as_view({'get': 'retrieve',
                                                                     'put': 'update',
                                                                     'delete': 'destroy'}), name='messages-detail'),
]
