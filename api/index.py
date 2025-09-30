from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np

app = FastAPI()

# Enable CORS for any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/")
async def telemetry(data: dict):
    regions = data.get("regions", [])
    threshold = data.get("threshold_ms", 180)

    # Example: load telemetry CSV from the bundle
    df = pd.read_csv("telemetry.csv")  # replace with actual path if needed

    # Filter by requested regions
    df = df[df["region"].isin(regions)]

    result = {}
    for region in regions:
        r = df[df["region"] == region]
        if not r.empty:
            avg_latency = r["latency_ms"].mean()
            p95_latency = np.percentile(r["latency_ms"], 95)
            avg_uptime = r["uptime"].mean()
            breaches = (r["latency_ms"] > threshold).sum()
        else:
            avg_latency = p95_latency = avg_uptime = breaches = 0

        result[region] = {
            "avg_latency": float(avg_latency),
            "p95_latency": float(p95_latency),
            "avg_uptime": float(avg_uptime),
            "breaches": int(breaches),
        }

    return result
