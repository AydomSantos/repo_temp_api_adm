import stripe
from fastapi import APIRouter, HTTPException, status
from app.config import settings
from app.models.payment import CheckoutRequest, CheckoutResponse
from app.services.database import insert_pedido, update_pedido_status, get_pedido_by_session

router = APIRouter(prefix="/pagamento", tags=["Pagamento"])

@router.post("/checkout", response_model=CheckoutResponse)
def create_checkout_session(data: CheckoutRequest):
    # Configura a chave do Stripe dinamicamente a cada requisição
    stripe.api_key = settings.stripe_api_key

    if not settings.stripe_api_key or "placeholder" in settings.stripe_api_key:
        print(f"DEBUG: Stripe Key atual: {settings.stripe_api_key}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Chave de API do Stripe não configurada corretamente.")

    if settings.stripe_api_key.startswith("pk_"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro de Configuração: Você configurou a Chave Pública (pk_...) no backend. O backend exige a Chave Secreta (sk_...)."
        )

    if not data.itens:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O carrinho não pode estar vazio.")

    try:
        line_items = []
        total_amount = 0

        # Formata os itens para o padrão do Stripe
        for item in data.itens:
            # Stripe trabalha com centavos (BRL), então multiplicamos por 100 e convertemos para int
            preco_centavos = int(item.preco_unitario * 100)
            total_amount += preco_centavos * item.quantidade
            
            line_items.append({
                'price_data': {
                    'currency': 'brl',
                    'product_data': {
                        'name': item.nome,
                    },
                    'unit_amount': preco_centavos,
                },
                'quantity': item.quantidade,
            })

        # Cria a sessão de checkout no Stripe
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'], # Aceitar cartão
            line_items=line_items,
            mode='payment',
            success_url='http://127.0.0.1:8000/pagamento/sucesso?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://127.0.0.1:8000/pagamento/cancelado',
            customer_email=data.email_cliente
        )

        # Salva o pedido no banco como "Pendente"
        insert_pedido({
            "email": data.email_cliente,
            "total": total_amount / 100, # Salva em reais
            "status": "pendente",
            "session_id": checkout_session.id,
            "itens": [item.model_dump() for item in data.itens]
        })

        return {"checkout_url": checkout_session.url, "session_id": checkout_session.id}

    except Exception as e:
        # Log do erro no console para facilitar a depuração
        print(f"Erro Stripe: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro ao processar pagamento: {str(e)}")

@router.get("/sucesso")
def payment_success(session_id: str):
    # Atualiza o status do pedido para pago
    update_pedido_status(session_id, "pago")
    return {"mensagem": "Pagamento realizado com sucesso!", "session_id": session_id}

@router.get("/cancelado")
def payment_cancel():
    return {"mensagem": "O pagamento foi cancelado pelo usuário."}