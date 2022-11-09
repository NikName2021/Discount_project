import asyncio
import schedule as schedule

from par import all_pars


def scheduler():
    """
    Функция - таймер
    """
    schedule.every(1).hour.do(all_pars)
    # каждые 10 минут запускаем фунцию "all_pars"
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    all_pars()
    asyncio.create_task(scheduler())