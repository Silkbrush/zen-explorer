class Profile:
    def __init__(self, name: str, profile_id: str):
        self.name: str = name
        self.id: str = profile_id

        if len(self.id) != 8:
            raise ValueError("id must be 8 characters")

    @classmethod
    def from_string(cls, profile_string: str):
        profile_id, profile_name = profile_string.split('.', 1)
        return cls(profile_name, profile_id)