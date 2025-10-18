#!/usr/bin/env python
import os
import sys
import django

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mini_soft.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Setup Django (so database settings are loaded)
    django.setup()


    # Continue with normal Django management command
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()



# #!/usr/bin/env python
# import os
# import sys
# import threading
# import django
# from django.db import connections

# def check_mssql():
#     def try_connect():
#         try:
#             conn = connections['mssql']
#             conn.ensure_connection()
#             print("✅ MSSQL connection OK")
#         except Exception as e:
#             print(f"❌ MSSQL connection FAILED: {str(e)}")
#             sys.stdout.flush()
#             sys.exit(1)  # Exit immediately if MSSQL cannot connect

#     # Run connection attempt in a thread
#     t = threading.Thread(target=try_connect)
#     t.start()
#     t.join(timeout=5)  # Wait max 5 seconds
#     if t.is_alive():
#         print("❌ MSSQL connection timed out after 5 seconds")
#         sys.stdout.flush()
#         sys.exit(1)  # Exit if timed out

# def main():
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mini_soft.settings')
#     try:
#         from django.core.management import execute_from_command_line
#     except ImportError as exc:
#         raise ImportError(
#             "Couldn't import Django. Are you sure it's installed and "
#             "available on your PYTHONPATH environment variable? Did you "
#             "forget to activate a virtual environment?"
#         ) from exc

#     # Setup Django
#     django.setup()

#     # ✅ Check MSSQL before proceeding
#     check_mssql()

#     # Run the management command if MSSQL is OK
#     execute_from_command_line(sys.argv)

# if __name__ == '__main__':
#     main()
