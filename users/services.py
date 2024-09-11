import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY

stripe.Product.create(name="Gold Plan")


def create_stripe_product(instance):
    """Создаем stripe продукт"""
    title_product = (
        f"{instance.paid_course}" if instance.paid_course else f"{instance.paid_lesson}"
    )
    stripe_product = stripe.Product.create(name=f"{title_product}")
    return stripe_product.get("id")


def create_stripe_price(payment_sum):
    """Создает цену в страйпе"""

    return stripe.Price.create(
        currency="usd",
        unit_amount=payment_sum * 100,
        product_data={"name": "Payment"},
    )


def create_stripe_session(price):
    """Создает сессию На оплату в страйпе"""

    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
