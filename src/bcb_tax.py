"""
Utilities to download PTAX (USD/BRL) rates from the BCB OData API.
"""

import datetime as _dt
from typing import List
import pandas as pd
import requests

API_URL_TEMPLATE = (
    "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
    "CotacaoDolarPeriodo(dataInicial='{start}',dataFinalCotacao='{end}')?"
    "$top=10000&$format=json"
)


def format_date_to_api(d: _dt.date) -> str:  # API date format mm-dd-yyyy
    return d.strftime("%m-%d-%Y")


def fetch_ptax(start: _dt.date, end: _dt.date) -> pd.DataFrame:  
    """Return PTAX buy/sell rates between *start* and *end* (inclusive)."""
    start_date_api = format_date_to_api(start)
    end_date_api = format_date_to_api(end)
    url = API_URL_TEMPLATE.format(start=start_date_api, end=end_date_api)
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    df = pd.json_normalize(resp.json()["value"])
    df = df.rename(
        columns={
            "cotacaoCompra": "cotacao_compra",
            "cotacaoVenda": "cotacao_venda",
            "dataHoraCotacao": "data_hora_cotacao",
        }
    )

    df["data_cotacao"] = pd.to_datetime(df["data_hora_cotacao"]).dt.date
    return df[
        ["data_cotacao", "cotacao_compra", "cotacao_venda", "data_hora_cotacao"]
    ]


if __name__ == "__main__":
    # Quick ad-hoc test: prints last 5 lines.
    _today = _dt.date.today()
    _df = fetch_ptax(_today - _dt.timedelta(days=10), _today)
    print(_df.tail())
