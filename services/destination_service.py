class DestinationService:
    """
    Business logic boundary for destination filtering/recommendations.
    """

    def __init__(self, repository):
        self.repository = repository

    def get_destinations(self):
        return self.repository.list_destinations()
