from dataclasses import dataclass


@dataclass(frozen=True)
class Constraint:
    """Provides data about the user's limitations."""
    name: str
    max_size_text_file: int
    max_count_text_file: int
    max_count_text_file_in_collection: int
    max_count_collections_created: int
    max_count_collections_subscriptions: int
    max_count_groups_created: int
    max_count_groups_subscriptions: int

    def __post_init__(self):
        fields_to_check = [
            "max_size_text_file",
            "max_count_text_file",
            "max_count_text_file_in_collection",
            "max_count_collections_created",
            "max_count_collections_subscriptions",
            "max_count_groups_created",
            "max_count_groups_subscriptions"
        ]
        for field_name in fields_to_check:
            value = getattr(self, field_name)
            if value == -1 or value > 0:
                raise ValueError(f"{field_name} The value can be -1 or greater than 0")
