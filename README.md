Market Strategy
===============

Overview
--------
- `market_strategy.py` computes a market-clearing matching on a bipartite graph encoded in `market.gml`.
- Sellers start with their listed price attribute; buyers bid using edge valuations and prices adjust until every buyer is matched.

Setup
-----
- Python 3.12+
- Create and activate a virtualenv: `python -m venv .venv && source .venv/bin/activate`
- Install dependencies from `requirements.txt`: `pip install -r requirements.txt`

Usage
-----
- `python ./market_strategy.py market.gml [--plot] [--interactive]`
- `--plot` draws the final graph with matched edges highlighted.
- `--interactive` prints per-round demand edges, price vector, and current matching.

Input Format
------------
- The GML file must tag sellers with `bipartite 0` and buyers with `bipartite 1`.
- Seller nodes may include an initial `price`; buyer-to-seller edges must define `valuation`.
- if there is no .gml file included this program will throw an error
