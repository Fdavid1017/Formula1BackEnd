import fastf1 as ff1
from resources import cache


class LoadLaps:
    @cache.cached(timeout=600, query_string=True)
    def load_laps_with_telemetry(self, gp_name, session_name):
        race = ff1.get_session(2021, gp_name, session_name)
        laps = race.load_laps(with_telemetry=True)

        return laps

    @cache.cached(timeout=600, query_string=True)
    def load_laps_without_telemetry(self, gp_name, session_name):
        race = ff1.get_session(2021, gp_name, session_name)
        laps = race.load_laps(with_telemetry=False)

        return laps
