class UserState:

    def __init__(self):

        self.search_type_selection_expected = False

        self.author_selection_expected = False
        self.title_selection_expected = False
        self.length_selection_expected = False

        self.page_selection_expected = False
        self.recording_selection_expected = False

        self.page = None
        self.strng = None
        self.column = None

        self.reversed_by_date_search_result = False

    def reset(self):

        self.search_type_selection_expected = False
        self.author_selection_expected = False
        self.title_selection_expected = False
        self.length_selection_expected = False
        self.page_selection_expected = False
        self.recording_selection_expected = False
        self.page = None
        self.strng = None
        self.column = None
