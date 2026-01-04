import argparse
from script.create_default_owner_user import create_default_admin_user
from script.create_default_mihan_wallet import create_default_mihan_wallet
from script.create_admins_from_file import create_branch_admins_from_file, create_agent_users_from_file
from script.migrate_user_role_data import migrate_user_role_data

parser = argparse.ArgumentParser(description='Script to run backend scripts easily.')

parser.add_argument('--default-admin', action='store_true', help='It will add default admin')
parser.add_argument('--migrate-admin', action='store_true', help='It will migrate supporter admins')
parser.add_argument('--default-wallet', action='store_true', help='It will add default wallet')
parser.add_argument('--file-branch-admin', action='store_true', help='It will add branch admins from excel files')
parser.add_argument('--file-agent-admin', action='store_true', help='It will add agent admins from excel files')

args = parser.parse_args()

if not args.default_admin and \
        not args.default_admin and \
        not args.file_branch_admin and \
        not args.migrate_admin and \
        not args.file_agent_admin:
    parser.print_help()

if args.default_admin:
    create_default_admin_user()

if args.migrate_admin:
    migrate_user_role_data()

if args.file_branch_admin:
    create_branch_admins_from_file()

if args.file_agent_admin:
    create_agent_users_from_file()

if args.default_wallet:
    create_default_mihan_wallet()
