from django.db import transaction
from .models import Contact
import re
from difflib import SequenceMatcher


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
    
    @staticmethod
    def bulk_unarchive(contact_ids):
        if not contact_ids:
            return {
                'success': False,
                'error': {
                    'code': 'EMPTY_SELECTION',
                    'message': 'Nenhum contacto selecionado para desarquivar'
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
        
        already_active = []
        to_unarchive = []
        
        for contact in contacts:
            if contact.is_active:
                already_active.append(contact.name)
            else:
                to_unarchive.append(contact)
        
        if already_active and not to_unarchive:
            return {
                'success': False,
                'error': {
                    'code': 'ALREADY_ACTIVE',
                    'message': 'Os contactos selecionados já estão ativos.',
                    'contacts': already_active
                }
            }
        
        with transaction.atomic():
            unarchived_count = 0
            for contact in to_unarchive:
                contact.is_active = True
                contact.save(update_fields=['is_active', 'updated_at'])
                unarchived_count += 1
        
        result = {
            'success': True,
            'unarchived_count': unarchived_count,
            'message': f'{unarchived_count} contacto(s) desarquivado(s) com sucesso'
        }
        
        if already_active:
            result['already_active'] = already_active
            result['warning'] = f'{len(already_active)} contacto(s) já estavam ativos'
        
        return result
    
    @staticmethod
    def find_potential_duplicates(contact_id):
        try:
            original = Contact.objects.get(id=contact_id, is_active=True)
        except Contact.DoesNotExist:
            return {
                'success': False,
                'error': {
                    'code': 'CONTACT_NOT_FOUND',
                    'message': 'Contacto não encontrado'
                }
            }
        
        all_contacts = Contact.objects.filter(is_active=True).exclude(id=contact_id)
        
        duplicates = []
        for candidate in all_contacts:
            score, matched_fields, details = ContactService._calculate_similarity_score(original, candidate)
            
            if score >= 8:
                duplicates.append({
                    'contact': {
                        'id': candidate.id,
                        'name': candidate.name,
                        'email': candidate.email,
                        'phone': candidate.phone,
                        'whatsapp': candidate.whatsapp,
                        'nif': candidate.nif,
                        'company': candidate.company.name if candidate.company else None,
                        'address': candidate.address,
                        'city': candidate.city,
                        'postal_code': candidate.postal_code,
                        'position': candidate.position
                    },
                    'score': score,
                    'matched_fields': matched_fields,
                    'details': details
                })
        
        duplicates.sort(key=lambda x: x['score'], reverse=True)
        duplicates = duplicates[:20]
        
        return {
            'success': True,
            'original': {
                'id': original.id,
                'name': original.name,
                'email': original.email,
                'phone': original.phone,
                'whatsapp': original.whatsapp,
                'nif': original.nif,
                'company': original.company.name if original.company else None
            },
            'duplicates': duplicates,
            'max_score': 71
        }
    
    @staticmethod
    def _calculate_similarity_score(original, candidate):
        score = 0
        matched_fields = []
        details = {}
        
        if original.nif and candidate.nif and original.nif.strip() == candidate.nif.strip():
            score += 15
            matched_fields.append('nif')
            details['nif'] = {'value': original.nif, 'points': 15}
        
        if original.phone and candidate.phone:
            norm_orig = ContactService._normalize_phone(original.phone)
            norm_cand = ContactService._normalize_phone(candidate.phone)
            if norm_orig == norm_cand:
                score += 12
                matched_fields.append('phone')
                details['phone'] = {'value': original.phone, 'points': 12}
        
        if original.whatsapp and candidate.whatsapp:
            norm_orig = ContactService._normalize_phone(original.whatsapp)
            norm_cand = ContactService._normalize_phone(candidate.whatsapp)
            if norm_orig == norm_cand:
                score += 10
                matched_fields.append('whatsapp')
                details['whatsapp'] = {'value': original.whatsapp, 'points': 10}
        
        name_score, name_type = ContactService._compare_names(original.name, candidate.name)
        if name_score > 0:
            score += name_score
            matched_fields.append('name')
            details['name'] = {'value': candidate.name, 'points': name_score, 'type': name_type}
        
        if original.company_id and candidate.company_id and original.company_id == candidate.company_id:
            score += 10
            matched_fields.append('company')
            details['company'] = {'value': original.company.name, 'points': 10}
        
        if original.address and candidate.address and original.address.strip().lower() == candidate.address.strip().lower():
            score += 5
            matched_fields.append('address')
            details['address'] = {'value': original.address, 'points': 5}
        
        if original.postal_code and candidate.postal_code and original.postal_code.strip() == candidate.postal_code.strip():
            score += 4
            matched_fields.append('postal_code')
            details['postal_code'] = {'value': original.postal_code, 'points': 4}
        
        if original.city and candidate.city and original.city.strip().lower() == candidate.city.strip().lower():
            score += 3
            matched_fields.append('city')
            details['city'] = {'value': original.city, 'points': 3}
        
        if original.position and candidate.position:
            pos_orig = original.position.strip().lower()
            pos_cand = candidate.position.strip().lower()
            if pos_orig == pos_cand:
                score += 2
                matched_fields.append('position')
                details['position'] = {'value': original.position, 'points': 2}
            elif SequenceMatcher(None, pos_orig, pos_cand).ratio() > 0.7:
                score += 1
                matched_fields.append('position')
                details['position'] = {'value': candidate.position, 'points': 1, 'type': 'similar'}
        
        return score, matched_fields, details
    
    @staticmethod
    def _compare_names(name1, name2):
        n1 = name1.lower().strip()
        n2 = name2.lower().strip()
        
        if n1 == n2:
            return 10, 'exact'
        
        words1 = set(n1.split())
        words2 = set(n2.split())
        
        if words1 == words2:
            return 7, 'inverted'
        
        common_words = words1 & words2
        if len(common_words) >= 2:
            return 5, 'partial'
        elif len(common_words) == 1:
            return 1, 'single_word'
        
        ratio = SequenceMatcher(None, n1, n2).ratio()
        if ratio > 0.8:
            return 4, 'similar'
        elif ratio > 0.6:
            return 2, 'somewhat_similar'
        
        return 0, 'different'
    
    @staticmethod
    def _normalize_phone(phone):
        return re.sub(r'[\s\-\(\)\+]', '', phone)
