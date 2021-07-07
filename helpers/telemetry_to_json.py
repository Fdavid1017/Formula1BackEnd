def telemetry_to_json(telemetry):
    # json_data = []
    # tel = telemetry
    data = {}

    if 'RPM' in telemetry.columns:
        data["RPM"] = telemetry['RPM'].tolist()

    if 'Speed' in telemetry.columns:
        data["Speed"] = telemetry['Speed'].tolist()

    if 'nGear' in telemetry.columns:
        data["nGear"] = telemetry['nGear'].tolist()

    if 'Throttle' in telemetry.columns:
        data["Throttle"] = telemetry['Throttle'].tolist()

    if 'Brake' in telemetry.columns:
        data["Brake"] = telemetry['Brake'].tolist()

    if 'DRS' in telemetry.columns:
        data["DRS"] = telemetry['DRS'].tolist()

    if 'Compound' in telemetry.columns:
        data["Compound"] = telemetry['Compound'].tolist()

    if 'TyreLife' in telemetry.columns:
        data["TyreLife"] = telemetry['TyreLife'].tolist()

    if 'TrackStatus' in telemetry.columns:
        data["TrackStatus"] = telemetry['TrackStatus'].tolist()

    if 'Distance' in telemetry.columns:
        data["Distance"] = telemetry['Distance'].tolist()

    if 'DriverAhead' in telemetry.columns:
        data["DriverAhead"] = telemetry['DriverAhead'].tolist()

    if 'Time' in telemetry.columns:
        data["Time"] = telemetry['Time'].tolist()
        for k in range(len(data["Time"])):
            data["Time"][k] = str(data["Time"][k])

    if 'SessionTime' in telemetry.columns:
        data["SessionTime"] = telemetry['SessionTime'].tolist()
        for k in range(len(data["SessionTime"])):
            data["SessionTime"][k] = str(data["SessionTime"][k])

    return data
