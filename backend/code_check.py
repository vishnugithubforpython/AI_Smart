from auth.utils import hash_password, verify_password

password = "Vishnu@123"

hashed = hash_password(password)

print(hashed)

print(verify_password(password, hashed))