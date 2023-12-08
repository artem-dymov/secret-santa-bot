class User:
    def __init__(self, id: int, tg_id: int, pib: str = None, phone_number: int = None,
                 nv_poshta_address: str = None, ukrposhta_index: int = None, wishes: str = None):
        self.id = id
        self.tg_id = id
        self.pib = pib
        self.phone_number = phone_number
        self.nv_poshta_address = nv_poshta_address
        self.ukrposhta_index = ukrposhta_index
        self.wishes = wishes
