"""
Data handlers for different business sectors
"""

from app.models.schemas import Sector
from app.data.hr_data import HRDataHandler
from app.data.sales_data import SalesDataHandler
from app.data.service_data import ServiceDataHandler
from app.data.finance_data import FinanceDataHandler


def get_data_handler(sector: Sector):
    """
    Get data handler for a specific sector
    
    Args:
        sector: Business sector
    
    Returns:
        Data handler instance
    """
    handlers = {
        Sector.HR: HRDataHandler(),
        Sector.SALES: SalesDataHandler(),
        Sector.SERVICE: ServiceDataHandler(),
        Sector.FINANCE: FinanceDataHandler()
    }
    
    return handlers.get(sector, HRDataHandler())

