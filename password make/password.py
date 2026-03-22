from werkzeug.security import generate_password_hash

# Generate the scrypt hash for 'admin123'
new_hash = generate_password_hash('admin123', method='scrypt')
print(new_hash)