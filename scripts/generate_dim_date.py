from datetime import datetime
import pandas as pd

start_date = "2024-01-01"
end_date = "2026-12-31"

dates = pd.date_range(start=start_date, end=end_date, freq="D")

rows = []

for d in dates:
    rows.append({
        "DateKey": int(d.strftime("%Y%m%d")),
        "Date": d.strftime("%Y-%m-%d"),
        "Year": d.year,
        "Quarter": f"Q{d.quarter}",
        "Month": d.month,
        "MonthName": d.strftime("%B"),
        "MonthShortName": d.strftime("%b"),
        "Week": int(d.strftime("%U")),
        "DayOfMonth": d.day,
        "DayOfWeek": d.isoweekday(),
        "DayName": d.strftime("%A"),
        "IsWeekend": d.isoweekday() >= 6
    })

df = pd.DataFrame(rows)

df.to_csv(
    "../data/master/DimDate.csv",
    index=False
)

print(f"Generated {len(df)} rows")
