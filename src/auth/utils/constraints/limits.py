from auth.utils.constraints.constraint import Constraint
# Класс для ограничений пользователя в соответствии с его статусом

class Limits:
    def __init__(self):
        self.constraints: dict[str, Constraint] = dict()

    def add_constraint(self,
                       name: str,
                       max_size_text_file: int,
                       max_count_text_file: int,
                       max_count_text_file_in_collection: int,
                       max_count_collections_created: int,
                       max_count_collections_subscriptions: int,
                       max_count_groups_created: int,
                       max_count_groups_subscriptions: int
                       ):
        """Sets limits."""
        constraint_obj = Constraint(name,
                                    max_size_text_file,
                                    max_count_text_file,
                                    max_count_text_file_in_collection,
                                    max_count_collections_created,
                                    max_count_collections_subscriptions,
                                    max_count_groups_created,
                                    max_count_groups_subscriptions

                                    )
        self.constraints[name] = constraint_obj

    def __str__(self):
        st = ""
        for key, value in self.constraints.items():
            st += f"{key}: {str(value)}\n"

        return st

    def __call__(self, status: str) -> Constraint:
        """Returns the constraint according to the status."""
        if status not in self.constraints:
            raise ValueError(f"There are no restrictions added to this {status}.")
        return self.constraints[status]
