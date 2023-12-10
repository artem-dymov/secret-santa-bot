class User:
    def __init__(self, id: int, tg_id: int, pib: str = None, phone_number: int = None,
                 nv_poshta_address: str = None, ukrposhta_index: int = None, wishes: str = None,
                 santa_id: int = None, user_to_gift: int = None):
        self.id = id
        self.tg_id = tg_id
        self.pib = pib
        self.phone_number = phone_number
        self.nv_poshta_address = nv_poshta_address
        self.ukrposhta_index = ukrposhta_index
        self.wishes = wishes

        self.santa_id = santa_id
        self.user_to_gift_id = user_to_gift
