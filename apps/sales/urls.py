from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    # ── Index ────────────────────────────────────────────────────────
    path('', views.sale_order_index, name='order_index'),

    # ── Create / Edit / Detail ───────────────────────────────────────
    path('nova/',               views.sale_order_create, name='order_create'),
    path('<uuid:pk>/',          views.sale_order_detail, name='order_detail'),
    path('<uuid:pk>/editar/',   views.sale_order_edit,   name='order_edit'),

    # ── State transitions ────────────────────────────────────────────
    path('<uuid:pk>/confirmar/', views.sale_order_confirm, name='order_confirm'),
    path('<uuid:pk>/entregar/',  views.sale_order_deliver, name='order_deliver'),
    path('<uuid:pk>/cancelar/',  views.sale_order_cancel,  name='order_cancel'),

    # ── Lines (AJAX) ─────────────────────────────────────────────────
    path('<uuid:pk>/linhas/adicionar/',                         views.sale_order_line_add,    name='order_line_add'),
    path('<uuid:pk>/linhas/<uuid:line_pk>/remover/',            views.sale_order_line_remove, name='order_line_remove'),
    path('<uuid:pk>/linhas/<uuid:line_pk>/actualizar/',         views.sale_order_line_update, name='order_line_update'),

    # ── Chatter ──────────────────────────────────────────────────────
    path('<uuid:pk>/notes/',                                    views.sale_order_notes_list,      name='order_notes_list'),
    path('<uuid:pk>/notes/create/',                             views.sale_order_note_create,     name='order_note_create'),
    path('<uuid:pk>/followers/',                                views.sale_order_followers_api,   name='order_followers_api'),
    path('<uuid:pk>/followers/<uuid:user_id>/remove/',          views.sale_order_follower_remove, name='order_follower_remove'),

    # ── Bulk actions (AJAX) ──────────────────────────────────────────
    path('bulk/arquivar/',    views.sale_order_bulk_archive,   name='order_bulk_archive'),
    path('bulk/desarquivar/', views.sale_order_bulk_unarchive, name='order_bulk_unarchive'),
    path('bulk/eliminar/',    views.sale_order_bulk_delete,    name='order_bulk_delete'),

    # ── Payment Terms ────────────────────────────────────────────────
    path('configuracao/condicoes-pagamento/',                                      views.payment_term_list,             name='payment_term_list'),
    path('configuracao/condicoes-pagamento/novo/',                                 views.payment_term_create,           name='payment_term_create'),
    path('configuracao/condicoes-pagamento/bulk/activar/',                         views.payment_term_bulk_activate,    name='payment_term_bulk_activate'),
    path('configuracao/condicoes-pagamento/bulk/desactivar/',                      views.payment_term_bulk_deactivate,  name='payment_term_bulk_deactivate'),
    path('configuracao/condicoes-pagamento/bulk/eliminar/',                        views.payment_term_bulk_delete,      name='payment_term_bulk_delete'),
    path('configuracao/condicoes-pagamento/<uuid:pk>/editar/',                     views.payment_term_edit,             name='payment_term_edit'),
    path('configuracao/condicoes-pagamento/<uuid:pk>/toggle/',                     views.payment_term_toggle,           name='payment_term_toggle'),
    path('configuracao/condicoes-pagamento/<uuid:pk>/eliminar/',                   views.payment_term_delete,           name='payment_term_delete'),
]
