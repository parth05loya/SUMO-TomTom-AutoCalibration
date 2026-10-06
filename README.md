# SUMO-TomTom-AutoCalibration

Automated calibration of a SUMO traffic simulation against TomTom traffic-aware travel-time observations.

## Workflow

TomTom Traffic API -> observed travel times -> Python -> geospatial matching -> SUMO/libsumo -> model comparison -> optimizer -> calibrated network/OD demand -> repeat.

## Current scope

- Load a SUMO `.net.xml` network.
- Read OD pairs from CSV.
- Query TomTom traffic-aware routing for observed OD travel times.
- Map OD coordinates to nearby SUMO edges.
- Run SUMO route-time primitives.
- Calculate MAE, RMSE, MAPE and bias.
- Coarse-to-fine parameter search.
- Streamlit UI for interactive experiments.

## Research architecture

1. Observation: collect TomTom travel times for representative OD pairs and target time periods.
2. Matching: map geographic observations to the directed SUMO network.
3. Simulation: run the same scenario in SUMO.
4. Objective: compare simulated and observed travel time.
5. Calibration: optimize selected network parameters, then OD-demand parameters.
6. Validation: evaluate on held-out OD pairs/time periods.

## Important modeling point

Travel-time observations alone do not uniquely identify demand and network parameters. Higher demand, lower capacity, lower speed, or signal effects can produce similar travel-time errors. Use staged calibration, regularization and independent validation.

## Repository structure

- `app/streamlit_app.py` - Streamlit interface
- `src/calibration/tomtom.py` - TomTom API client
- `src/calibration/network.py` - SUMO network utilities
- `src/calibration/sumo.py` - SUMO/libsumo execution primitives
- `src/calibration/metrics.py` - travel-time metrics
- `src/calibration/optimizer.py` - deterministic parameter search
- `src/calibration/od.py` - OD validation/loading
- `src/calibration/pipeline.py` - observation/matching pipeline
- `config/default.yaml` - experiment defaults
- `examples/example_od.csv` - OD example
- `tests/` - unit tests

## Requirements

Python 3.10+, SUMO with its Python tools (`sumolib`, `traci`, preferably `libsumo`), and TomTom API access for the routing endpoint used by your account.

Install:

    git clone https://github.com/parth05loya/SUMO-TomTom-AutoCalibration.git
    cd SUMO-TomTom-AutoCalibration
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Environment variables:

    TOMTOM_API_KEY=your_api_key
    SUMO_HOME=/path/to/sumo
    SUMO_BINARY=sumo
    USE_LIBSUMO=true

Never commit real API keys.

## OD CSV format

Required columns: `od_id`, `origin_lon`, `origin_lat`, `destination_lon`, `destination_lat`.

Example:

    od_id,origin_lon,origin_lat,destination_lon,destination_lat
    1,75.8577,22.7196,75.8640,22.7275
    2,75.8500,22.7100,75.8800,22.7350

## Run the UI

    streamlit run app/streamlit_app.py

The interface collects TomTom observations and maps OD locations to SUMO edges. The simulation/optimization modules are kept separate so they can be expanded into full congestion/demand calibration.

## Metrics

For observed travel time To and simulated travel time Ts:

- error = Ts - To
- MAE = mean(abs(error))
- RMSE = sqrt(mean(error^2))
- MAPE = mean(abs(error / To)) * 100
- Bias = mean(error)

## Limitations

TomTom route observations are not automatically equivalent to link-level SUMO observations. Production studies should map-match route geometry to directed SUMO edges before making link-level claims.

TomTom is an external traffic-data source; preserve observation time, endpoint assumptions, network version, SUMO version, OD split and calibration configuration for reproducibility.

TomTom endpoints, quotas, authentication and free-tier terms can change. Follow the current TomTom developer documentation and your account plan.

## Roadmap

- Route-geometry map matching
- Explicit congestion simulation with route/flow files
- Edge-class speed calibration
- Capacity calibration
- Signal calibration
- OD-demand calibration
- Joint network + OD optimization
- Differential evolution / Bayesian optimization
- Hold-out validation dashboard
- Batch libsumo execution
- Experiment reports
- Additional traffic-data providers

## Research applications

The project can support studies of manual vs automated SUMO calibration, network-only vs joint network/demand calibration, observation density, transferability across time periods and optimizer comparison.

## License

MIT. See `LICENSE`.

## Author

Parth Loya

https://github.com/parth05loya/SUMO-TomTom-AutoCalibration
