from src.manager import Manager
from src.models import Parameters

def test_get_tax(tmp_path):
    apartments = tmp_path / "apartments.json"
    tenants = tmp_path / "tenants.json"
    bills = tmp_path / "bills.json"
    transfers = tmp_path / "transfers.json"

    apartments.write_text("{}")
    tenants.write_text("{}")
    bills.write_text("[]")

    transfers.write_text("""
    [
        {
            "tenant": "Jan",
            "date": "2024-03-05",
            "settlement_year": 2024,
            "settlement_month": 3,
            "amount_pln": 1000
        },
        {
            "tenant": "Anna",
            "date": "2024-03-07",
            "settlement_year": 2024,
            "settlement_month": 3,
            "amount_pln": 500
        }
    ]
    """)

    params = Parameters(
        apartments_json_path=str(apartments),
        tenants_json_path=str(tenants),
        bills_json_path=str(bills),
        transfers_json_path=str(transfers)
    )

    manager = Manager(params)

    tax = manager.get_tax(2024, 3, 0.085)

    assert tax == 128
