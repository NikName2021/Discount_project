import asyncio
import schedule as schedule

from par import all_pars


def scheduler():
    """
    Функция - таймер
    """
    print(12)
    schedule.every(10).minutes.do(all_pars)
    # каждые 10 минут запускаем фунцию "all_pars"
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    all_pars()
    asyncio.create_task(scheduler())