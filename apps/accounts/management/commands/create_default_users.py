from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.core.models import Company

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates default users (admin and manager) if they do not exist'

    def add_arguments(self, parser):
        parser.add_argument(
            '--admin-username',
            type=str,
            default='cubix',
            help='Username for admin user (default: cubix)'
        )
        parser.add_argument(
            '--admin-password',
            type=str,
            default='cubix123',
            help='Password for admin user (default: cubix123)'
        )
        parser.add_argument(
            '--manager-username',
            type=str,
            default='daisy',
            help='Username for manager user (default: daisy)'
        )
        parser.add_argument(
            '--manager-password',
            type=str,
            default='torres',
            help='Password for manager user (default: torres)'
        )

    def handle(self, *args, **options):
        admin_username = options['admin_username']
        admin_password = options['admin_password']
        manager_username = options['manager_username']
        manager_password = options['manager_password']
        
        # Get default company
        default_company = Company.objects.filter(name='Fuet Mágico').first()
        
        if not default_company:
            self.stdout.write(
                self.style.WARNING(
                    'Default company "Fuet Mágico" not found. Run "create_default_company" first.'
                )
            )
            return
        
        created_users = []
        
        # Create Admin User
        if User.objects.filter(username=admin_username).exists():
            self.stdout.write(
                self.style.WARNING(f'Admin user "{admin_username}" already exists.')
            )
        else:
            admin_user = User.objects.create_superuser(
                username=admin_username,
                email='admin@fuetmagico.pt',
                password=admin_password,
                first_name='Administrator',
                last_name='System',
                role=User.ADMIN
            )
            admin_user.default_company = default_company
            admin_user.save()
            admin_user.companies.add(default_company)
            
            created_users.append(f'Admin: {admin_username}')
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Admin user created: {admin_username} (password: {admin_password})'
                )
            )
        
        # Create Manager User
        if User.objects.filter(username=manager_username).exists():
            self.stdout.write(
                self.style.WARNING(f'Manager user "{manager_username}" already exists.')
            )
        else:
            manager_user = User.objects.create_user(
                username=manager_username,
                email='manager@fuetmagico.pt',
                password=manager_password,
                first_name='Manager',
                last_name='Default',
                role=User.MANAGER,
                is_staff=True  # Can access admin
            )
            manager_user.default_company = default_company
            manager_user.save()
            manager_user.companies.add(default_company)
            
            created_users.append(f'Manager: {manager_username}')
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Manager user created: {manager_username} (password: {manager_password})'
                )
            )
        
        # Summary
        if created_users:
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('=' * 60))
            self.stdout.write(self.style.SUCCESS('DEFAULT USERS CREATED SUCCESSFULLY'))
            self.stdout.write(self.style.SUCCESS('=' * 60))
            for user_info in created_users:
                self.stdout.write(self.style.SUCCESS(f'  • {user_info}'))
            self.stdout.write(self.style.SUCCESS('=' * 60))
            self.stdout.write('')
            self.stdout.write(
                self.style.WARNING('⚠️  IMPORTANT: Change these passwords in production!')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('All default users already exist.')
            )
