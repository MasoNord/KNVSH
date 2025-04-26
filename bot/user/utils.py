

# Класс для хранения состояний отображаемых объектов (мероприятия и вакансия)
class DisplayObjects:
    adjust_vacancies=[]
    adjust_events=[]
    current_event_index = 0
    current_vacancy_index = 0, 

    def __init__(self, adjust_vacancies, adjust_events, current_event_index, current_vacancy_index):
        self.adjust_events=adjust_events
        self.adjust_vacancies = adjust_vacancies
        self.current_event_index = current_event_index
        self.current_vacancy_index = current_vacancy_index

    