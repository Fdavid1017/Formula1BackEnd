import fastf1 as ff1


def get_weekend_results(weekend_name):
    weekend = ff1.get_session(2021, weekend_name)

    fp1_results = get_fastest_laps_from_session(weekend.get_practice(1))
    fp2_results = get_fastest_laps_from_session(weekend.get_practice(2))
    fp3_results = get_fastest_laps_from_session(weekend.get_practice(3))
    quali = get_fastest_laps_from_session(weekend.get_quali())
    race = get_fastest_laps_from_session(weekend.get_race())


def get_fastest_laps_from_session(session):
    session.load_laps()
    sorted_laps = session.laps.sort_values(by='LapTime')
    unique = sorted_laps.drop_duplicates(subset=['DriverNumber'])

    # session_results=[]
    #
    # for index, row in unique.iterrows():
    #     print(row["Driver"])

    return unique
