from django.db import transaction
from .models import Contact


class ContactService:
    
    @staticmethod
    def bulk_archive(contact_ids):
        if not contact_ids:
            return {
                'success': False,
                'error': {
                    'code': 'EMPTY_SELECTION',
                    'message': 'Nenhum contacto selecionado para arquivar'
                }
            }
        
        contacts = Contact.objects.filter(id__in=contact_ids)
        
        if not contacts.exists():
            return {
                'success': False,
                'error': {
                    'code': 'CONTACTS_NOT_FOUND',
                    'message': 'Nenhum contacto válido encontrado'
                }
            }
        
        already_archived = []
        to_archive = []
        
        for contact in contacts:
            if not contact.is_active:
                already_archived.append(contact.name)
            else:
                to_archive.append(contact)
        
        if already_archived and not to_archive:
            return {
                'success': False,
                'error': {
                    'code': 'ALREADY_ARCHIVED',
                    'message': 'Os contactos selecionados já estão arquivados. Use a opção desarquivar se pretende restaurá-los.',
                    'contacts': already_archived
                }
            }
        
        with transaction.atomic():
            archived_count = 0
            for contact in to_archive:
                contact.is_active = False
                contact.save(update_fields=['is_active', 'updated_at'])
                archived_count += 1
        
        result = {
            'success': True,
            'archived_count': archived_count,
            'message': f'{archived_count} contacto(s) arquivado(s) com sucesso'
        }
        
        if already_archived:
            result['already_archived'] = already_archived
            result['warning'] = f'{len(already_archived)} contacto(s) já estavam arquivados'
        
        return result
