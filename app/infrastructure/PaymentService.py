class PaymentService:
    def pay(self, user_id: str, amount: int) -> bool:
        """決済処理。成功ならTrue、失敗ならFalse"""
        raise NotImplementedError

class MockPaymentService(PaymentService):
    def pay(self, user_id: str, amount: int) -> bool:
        print(f"Mock payment for user_id={user_id}, amount={amount}")
        return True