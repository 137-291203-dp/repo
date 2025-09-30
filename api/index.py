from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import statistics

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample telemetry data
TELEMETRY_DATA = [
    {"region": "apac", "service": "recommendations", "latency_ms": 130.69, "uptime_pct": 99.149, "timestamp": 20250301},
    {"region": "apac", "service": "support", "latency_ms": 214.55, "uptime_pct": 97.816, "timestamp": 20250302},
    {"region": "apac", "service": "support", "latency_ms": 191.46, "uptime_pct": 97.264, "timestamp": 20250303},
    {"region": "apac", "service": "checkout", "latency_ms": 171.88, "uptime_pct": 98.066, "timestamp": 20250304},
    {"region": "apac", "service": "analytics", "latency_ms": 161.55, "uptime_pct": 97.369, "timestamp": 20250305},
    {"region": "apac", "service": "support", "latency_ms": 160.9, "uptime_pct": 97.862, "timestamp": 20250306},
    {"region": "apac", "service": "checkout", "latency_ms": 124.36, "uptime_pct": 98.953, "timestamp": 20250307},
    {"region": "apac", "service": "support", "latency_ms": 217.17, "uptime_pct": 98.646, "timestamp": 20250308},
    {"region": "apac", "service": "payments", "latency_ms": 164.06, "uptime_pct": 98.939, "timestamp": 20250309},
    {"region": "apac", "service": "catalog", "latency_ms": 201.67, "uptime_pct": 97.236, "timestamp": 20250310},
    {"region": "apac", "service": "checkout", "latency_ms": 222.02, "uptime_pct": 99.039, "timestamp": 20250311},
    {"region": "apac", "service": "recommendations", "latency_ms": 132.36, "uptime_pct": 98.796, "timestamp": 20250312},
    {"region": "emea", "service": "checkout", "latency_ms": 217.18, "uptime_pct": 98.091, "timestamp": 20250301},
    {"region": "emea", "service": "payments", "latency_ms": 163.14, "uptime_pct": 99.233, "timestamp": 20250302},
    {"region": "emea", "service": "payments", "latency_ms": 202.45, "uptime_pct": 98.179, "timestamp": 20250303},
    {"region": "emea", "service": "recommendations", "latency_ms": 131.84, "uptime_pct": 98.743, "timestamp": 20250304},
    {"region": "emea", "service": "support", "latency_ms": 221.43, "uptime_pct": 99.099, "timestamp": 20250305},
    {"region": "emea", "service": "payments", "latency_ms": 126.04, "uptime_pct": 98.867, "timestamp": 20250306},
    {"region": "emea", "service": "recommendations", "latency_ms": 125.34, "uptime_pct": 98.784, "timestamp": 20250307},
    {"region": "emea", "service": "analytics", "latency_ms": 217.81, "uptime_pct": 98.066, "timestamp": 20250308},
    {"region": "emea", "service": "catalog", "latency_ms": 151.94, "uptime_pct": 98.369, "timestamp": 20250309},
    {"region": "emea", "service": "analytics", "latency_ms": 145.37, "uptime_pct": 99.437, "timestamp": 20250310},
    {"region": "emea", "service": "checkout", "latency_ms": 184.09, "uptime_pct": 98.269, "timestamp": 20250311},
    {"region": "emea", "service": "recommendations", "latency_ms": 181.51, "uptime_pct": 98.251, "timestamp": 20250312},
    {"region": "amer", "service": "catalog", "latency_ms": 192.44, "uptime_pct": 98.446, "timestamp": 20250301},
    {"region": "amer", "service": "recommendations", "latency_ms": 143.18, "uptime_pct": 98.815, "timestamp": 20250302},
    {"region": "amer", "service": "catalog", "latency_ms": 173.78, "uptime_pct": 97.244, "timestamp": 20250303},
    {"region": "amer", "service": "catalog", "latency_ms": 215.91, "uptime_pct": 97.34, "timestamp": 20250304},
    {"region": "amer", "service": "recommendations", "latency_ms": 162.48, "uptime_pct": 98.998, "timestamp": 20250305},
    {"region": "amer", "service": "catalog", "latency_ms": 187.35, "uptime_pct": 97.391, "timestamp": 20250306},
    {"region": "amer", "service": "catalog", "latency_ms": 138.7, "uptime_pct": 98.393, "timestamp": 20250307},
    {"region": "amer", "service": "recommendations", "latency_ms": 107.26, "uptime_pct": 98.007, "timestamp": 20250308},
    {"region": "amer", "service": "payments", "latency_ms": 127.9, "uptime_pct": 98.959, "timestamp": 20250309},
    {"region": "amer", "service": "recommendations", "latency_ms": 219.87, "uptime_pct": 98.95, "timestamp": 20250310},
    {"region": "amer", "service": "recommendations", "latency_ms": 190.91, "uptime_pct": 97.934, "timestamp": 20250311},
    {"region": "amer", "service": "checkout", "latency_ms": 211.66, "uptime_pct": 98.78, "timestamp": 20250312}
]

class AnalyticsRequest(BaseModel):
    regions: list[str]
    threshold_ms: float

@app.get("/")
def read_root():
    return {"message": "Analytics API - Use POST /analytics"}

@app.post("/analytics")
def analyze_telemetry(request: AnalyticsRequest):
    result = {}
    
    for region in request.regions:
        # Filter data for this region
        region_data = [d for d in TELEMETRY_DATA if d["region"] == region]
        
        if not region_data:
            continue
        
        # Extract latencies and uptimes
        latencies = [d["latency_ms"] for d in region_data]
        uptimes = [d["uptime_pct"] for d in region_data]
        
        # Calculate metrics
        avg_latency = statistics.mean(latencies)
        p95_latency = statistics.quantiles(latencies, n=20)[18]  # 95th percentile
        avg_uptime = statistics.mean(uptimes)
        breaches = sum(1 for lat in latencies if lat > request.threshold_ms)
        
        result[region] = {
            "avg_latency": round(avg_latency, 2),
            "p95_latency": round(p95_latency, 2),
            "avg_uptime": round(avg_uptime, 3),
            "breaches": breaches
        }
    
    return result
