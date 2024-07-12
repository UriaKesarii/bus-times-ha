#!/usr/bin/env python3
import sys
import json
from datetime import datetime
import asyncio
import aiohttp
from typing import List, Dict

async def get_station_data(session: aiohttp.ClientSession, station: str) -> Dict:
    url = f"https://app.busnearby.co.il/stopSearch?query={station}&locale=he"
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.json()

async def get_bus_times_data(session: aiohttp.ClientSession, stop_id: str, current_time: int) -> List[Dict]:
    url = f"https://api.busnearby.co.il/directions/index/stops/1:{stop_id}/stoptimes?numberOfDepartures=1&timeRange=86400&startTime={current_time}&locale=he"
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.json()

async def get_bus_times(station: str, bus_lines: str, stop_id: str = None, stop_name: str = None):
    bus_lines = set(bus_lines.split(','))
    current_time = int(datetime.now().timestamp())
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://app.busnearby.co.il/",
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            if not stop_id:
                station_data = await get_station_data(session, station)
                if not station_data:
                    print("Station not found")
                    return

                stop_id = station_data[0]['stop_id']
                stop_name = station_data[0]['stop_name']
            times_data = await get_bus_times_data(session, stop_id, current_time)

            all_buses = [
                {
                    "lineNumber": bus['times'][0]['routeShortName'],
                    "arrivalSeconds": (bus['times'][0]['serviceDay'] + bus['times'][0]['realtimeArrival']) - current_time
                }
                for bus in times_data
                if (bus['times'][0]['serviceDay'] + bus['times'][0]['realtimeArrival']) - current_time >= 0
            ]

            filtered_buses = [bus for bus in all_buses if bus['lineNumber'] in bus_lines]

            # If any specified bus line is not found, return all buses
            if len(filtered_buses) < len(bus_lines):
                result = all_buses
            else:
                result = filtered_buses

            result.sort(key=lambda x: x['arrivalSeconds'])

            final_result = {
                "stationName": stop_name or "",
                "time": f"{datetime.now()}",
                "buses": result
            }

            print(json.dumps(final_result, indent=2, ensure_ascii=False))
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            print(f"Error fetching or decoding data: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 5:
        print("Usage: ./get_bus_times.py <station_number> <bus_lines> [stop_id] [stop_name]")
        sys.exit(1)

    station = sys.argv[1]
    bus_lines = sys.argv[2]
    stop_id = None
    stop_name = None
    if len(sys.argv) >= 4:
        stop_id = sys.argv[3]
    if len(sys.argv) == 5:
        stop_name = sys.argv[4]
    asyncio.run(get_bus_times(station, bus_lines, stop_id, stop_name))