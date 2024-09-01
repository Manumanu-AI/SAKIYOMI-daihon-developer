import datetime
from infrastructure.performance_repository import PerformanceRepository

class PerformanceService:
    def __init__(self, user_id: str):
        self.repository = PerformanceRepository(user_id)

    def log_feed_run(self, date: datetime.date, count: int = 1):
        return self.repository.log_run('feed_run', date, count)

    def log_reel_run(self, date: datetime.date, count: int = 1):
        return self.repository.log_run('reel_run', date, count)

    def log_feed_theme_run(self, date: datetime.date, count: int = 1):
        return self.repository.log_run('feed_theme_run', date, count)

    def log_reel_theme_run(self, date: datetime.date, count: int = 1):
        return self.repository.log_run('reel_theme_run', date, count)

    def log_data_analysis_run(self, date: datetime.date, count: int = 1):
        return self.repository.log_run('data_analysis_run', date, count)

    def get_feed_run_count(self, date: datetime.date):
        return self.repository.get_run_count('feed_run', date)

    def get_reel_run_count(self, date: datetime.date):
        return self.repository.get_run_count('reel_run', date)

    def list_all_runs(self, date: datetime.date):
        return self.repository.list_all_runs(date)
