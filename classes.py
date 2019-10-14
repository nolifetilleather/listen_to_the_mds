class User:

    def __init__(
        self,
        telegram_id,
    ):
        self.telegram_id = telegram_id

        self.sort_type_selection_expected = False

        self.author_selection_expected = False
        self.title_selection_expected = False
        self.length_selection_expected = False

        self.page_selection_expected = False
        self.recording_selection_expected = False

        self.page = 0
        self.strng = ''

        self.reversed_by_date_search_result = False
