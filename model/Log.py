
class Log:
    def __init__(user_fk, type_of_log):
        self.user_fk = user_fk
        self.type = type_of_log
        self.time = strftime('%Y-%m-%d %H:%M:%S', localtime())
