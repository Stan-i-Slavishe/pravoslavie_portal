# Database Models Schema

## Core App
- Category (id, name, slug, description, created_at)
- Tag (id, name, slug, color)

## Stories App  
- Story (id, title, slug, description, youtube_embed, category, tags, views_count, created_at)

## Fairy Tales App ⭐ КЛЮЧЕВОЙ МОДУЛЬ
- FairyTale (id, title, slug, content, age_group, therapeutic_goal, audio_file)
- FairyTaleCategory (id, name, description, color_code)
- AgeGroup (id, name, min_age, max_age, description)

## Books App
- Book (id, title, slug, description, cover_image, pdf_file, price, category)
- BookReview (id, book, user, rating, comment, created_at)
- BookRating (id, book, user, rating)

## Shop App - E-COMMERCE СИСТЕМА
- Product (id, name, slug, description, price, product_type, digital_file)
- Cart (id, user, created_at, updated_at)
- CartItem (id, cart, product, quantity)
- Order (id, user, total_amount, status, created_at)
- OrderItem (id, order, product, quantity, price)
- Purchase (id, user, product, order, download_count, purchased_at)
- Discount (id, code, discount_type, value, active, valid_until)

## Accounts App
- CustomUser (extends AbstractUser)
- UserProfile (id, user, bio, avatar, preferences)

## Subscriptions App
- Subscription (id, name, price, duration, features)
- UserSubscription (id, user, subscription, start_date, end_date, active)