from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    # ── Index ────────────────────────────────────────────────────────
    path('', views.sale_order_index, name='order_index'),

    # ── Create / Edit / Detail ───────────────────────────────────────
    path('new/',               views.sale_order_create, name='order_create'),
    path('<uuid:pk>/',          views.sale_order_detail, name='order_detail'),
    path('<uuid:pk>/edit/',    views.sale_order_edit,   name='order_edit'),

    # ── Report ───────────────────────────────────────────────────────
    path('<uuid:pk>/report/',                  views.sale_order_quotation_report,        name='order_quotation_report'),
    path('<uuid:pk>/send-quotation/',          views.sale_order_send_quotation,          name='order_send_quotation'),
    path('<uuid:pk>/quotation-email-compose/', views.sale_order_quotation_email_compose, name='order_quotation_email_compose'),

    # ── State transitions ────────────────────────────────────────────
    path('<uuid:pk>/confirm/', views.sale_order_confirm, name='order_confirm'),
    path('<uuid:pk>/deliver/', views.sale_order_deliver, name='order_deliver'),
    path('<uuid:pk>/cancel/',  views.sale_order_cancel,  name='order_cancel'),

    # ── Lines (AJAX) ─────────────────────────────────────────────────
    path('<uuid:pk>/lines/add/',                              views.sale_order_line_add,    name='order_line_add'),
    path('<uuid:pk>/lines/<uuid:line_pk>/remove/',            views.sale_order_line_remove, name='order_line_remove'),
    path('<uuid:pk>/lines/<uuid:line_pk>/update/',            views.sale_order_line_update, name='order_line_update'),

    # ── Chatter ──────────────────────────────────────────────────────
    path('<uuid:pk>/notes/',                                    views.sale_order_notes_list,      name='order_notes_list'),
    path('<uuid:pk>/notes/create/',                             views.sale_order_note_create,     name='order_note_create'),
    path('<uuid:pk>/followers/',                                views.sale_order_followers_api,   name='order_followers_api'),
    path('<uuid:pk>/followers/<uuid:user_id>/remove/',          views.sale_order_follower_remove, name='order_follower_remove'),

    # ── Signature Portal (public — no login required) ───────────────
    path('orcamento/<str:token>/',           views.quotation_sign,        name='quotation_sign'),
    path('orcamento/<str:token>/submeter/',  views.quotation_sign_submit, name='quotation_sign_submit'),
    path('orcamento/<str:token>/done/',      views.quotation_sign_done,   name='quotation_sign_done'),
    path('orcamento/termos/',               views.quotation_terms,       name='quotation_terms'),

    # ── Bulk actions (AJAX) ──────────────────────────────────────────
    path('bulk/archive/',    views.sale_order_bulk_archive,   name='order_bulk_archive'),
    path('bulk/unarchive/', views.sale_order_bulk_unarchive, name='order_bulk_unarchive'),
    path('bulk/delete/',    views.sale_order_bulk_delete,    name='order_bulk_delete'),

    # ── Payment Terms ────────────────────────────────────────────────
    path('config/payment-terms/',                                      views.payment_term_list,             name='payment_term_list'),
    path('config/payment-terms/new/',                                  views.payment_term_create,           name='payment_term_create'),
    path('config/payment-terms/bulk/activate/',                        views.payment_term_bulk_activate,    name='payment_term_bulk_activate'),
    path('config/payment-terms/bulk/deactivate/',                      views.payment_term_bulk_deactivate,  name='payment_term_bulk_deactivate'),
    path('config/payment-terms/bulk/delete/',                          views.payment_term_bulk_delete,      name='payment_term_bulk_delete'),
    path('config/payment-terms/<uuid:pk>/edit/',                       views.payment_term_edit,             name='payment_term_edit'),
    path('config/payment-terms/<uuid:pk>/toggle/',                     views.payment_term_toggle,           name='payment_term_toggle'),
    path('config/payment-terms/<uuid:pk>/delete/',                     views.payment_term_delete,           name='payment_term_delete'),
]
