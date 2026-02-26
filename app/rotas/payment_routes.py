import stripe
from fastapi import APIRouter, HTTPException, status

from app.config import settings
from app.models.payment import CheckoutRequest, CheckoutResponse
from app.services.database import insert_pedido, update_pedido_status

router = APIRouter(prefix="/pagamento", tags=["Pagamento"])


@router.post("/checkout", response_model=CheckoutResponse)
def create_checkout_session(data: CheckoutRequest):
    stripe.api_key = settings.stripe_api_key

    if not settings.stripe_api_key or "placeholder" in settings.stripe_api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Chave de API do Stripe nao configurada.",
        )

    if settings.stripe_api_key.startswith("pk_"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Backend exige chave secreta Stripe (sk_...).",
        )

    if not data.itens:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O carrinho nao pode estar vazio.")

    try:
        line_items = []
        total_amount = 0

        for item in data.itens:
            preco_centavos = int(item.preco_unitario * 100)
            total_amount += preco_centavos * item.quantidade
            line_items.append(
                {
                    "price_data": {
                        "currency": "brl",
                        "product_data": {"name": item.nome},
                        "unit_amount": preco_centavos,
                    },
                    "quantity": item.quantidade,
                }
            )

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url="http://127.0.0.1:8000/pagamento/sucesso?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://127.0.0.1:8000/pagamento/cancelado",
            customer_email=data.email_cliente,
        )

        insert_pedido(
            {
                "email": data.email_cliente,
                "total": total_amount / 100,
                "status": "pendente",
                "session_id": checkout_session.id,
                "itens": [item.model_dump() for item in data.itens],
            }
        )

        return {"checkout_url": checkout_session.url, "session_id": checkout_session.id}

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao processar pagamento.",
        )


@router.get("/sucesso")
def payment_success(session_id: str):
    update_pedido_status(session_id, "pago")
    return {"mensagem": "Pagamento realizado com sucesso!", "session_id": session_id}


@router.get("/cancelado")
def payment_cancel():
    return {"mensagem": "O pagamento foi cancelado pelo usuario."}
