# =============================================
# VAPID KEYS FOR WEB PUSH NOTIFICATIONS
# =============================================

# VAPID ключи для push-уведомлений
VAPID_PRIVATE_KEY = "MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgCokGsUojgTOoV261HRewKMAslomBJpo0JWp0iFsDEkyhRANCAASLSHKMWXcz/3F162RYJVy0n1MqoZuPo+ku2cu1Ms1xAXR8Y33vJzw8f+AYzuIcdS5dga9amzXvyyWh/JdnnSyW"
VAPID_PUBLIC_KEY = "BItIcoxZdzP/cXXrZFglXLSfUyqhm4+j6S7Zy7UyzXEBdHxjfe8nPDx/4BjO4hx1Ll2Br1qbNe/LJaH8l2edLJY="
VAPID_ADMIN_EMAIL = "admin@dobrist.com"

# Настройки для webpush
WEBPUSH_SETTINGS = {
    "VAPID_PUBLIC_KEY": VAPID_PUBLIC_KEY,
    "VAPID_PRIVATE_KEY": VAPID_PRIVATE_KEY,
    "VAPID_ADMIN_EMAIL": VAPID_ADMIN_EMAIL
}
