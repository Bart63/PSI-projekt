class API:
    data = []

    @classmethod
    def update_field(cls, field_name, new_value):
        setattr(cls, field_name, new_value)

    @classmethod
    def update_data(cls, new_data):
        cls.data = new_data
