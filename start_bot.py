import time
import functions as fnc

module_name = 'start_bot'

def start_bot():
    try:
        msg = (
            'Попытка запуска main.py'
        )
        fnc.log_write(module_name, msg)
        import main
    except Exception as e:
        err_msg = (
            'ОШИБКА!\n'
            f'{e.__class__}\n'
            f'{e}'
        )
        fnc.log_write(module_name, err_msg)
        time.sleep(10)
        start_bot()

start_bot()