from fastapi import FastAPI, Query
from entity.models import Information
from datetime import date, datetime
import service.cbrf as cbrf
from settings import settings

information = Information(
    version=settings.VERSION,
    service='currency',
    author='m.antropov'
)

today = date.today()

def setup_routes(app: FastAPI):
    @app.get("/info")
    async def get_info():
        """
        Endpoint to retrieve information about the app.

        Returns:
            Information: Version, service name, and author of the app.
        """
        return information

    @app.get("/info/currency")
    async def get_currency(
        date: str = Query(None, description="date in YYYY-MM-DD format"),
        currency: str = Query(None, description="currency corresponding ISO 4217 standard")
    ):
        """
        Endpoint to fetch the exchange rate of the specified currency for the specified date.

        Args:
            date (str, optional): Date to retrieve exchange rate of currency for, current date will be used, if date is not specified.
            currency (str, optional): Name of the currency corresponding ISO 4217 standard, all currencies available for the Cental Bank of the Russian Federation will be used.

        Returns:
            current_value: Exchange rate of the specified currency for the specified date.
        """
        current_value = cbrf.exchange_rate(date, currency)
        return current_value