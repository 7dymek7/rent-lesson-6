from src.manager import Manager
from src.models import Parameters

def test_get_debtors(tmp_path):
    apartments = tmp_path / "apartments.json"
    tenants = tmp_path / "tenants.json"
    bills = tmp_path / "bills.json"
    transfers = tmp_path / "transfers.json"

    apartments.write_text("""
    {
        "A1": {
            "key": "A1",
            "name": "Mieszkanie 1",
            "location": "Test City",
            "area_m2": 50,
            "rooms": {}
        }
    }
    """)

    tenants.write_text("""
    {
        "T1": {
            "name": "Jan",
            "apartment": "A1",
            "room": "R1",
            "rent_pln": 150,
            "deposit_pln": 500,
            "date_agreement_from": "2024-01-01",
            "date_agreement_to": "2024-12-31"
        },
        "T2": {
            "name": "Anna",
            "apartment": "A1",
            "room": "R2",
            "rent_pln": 150,
            "deposit_pln": 500,
            "date_agreement_from": "2024-01-01",
            "date_agreement_to": "2024-12-31"
        }
    }
    """)

    bills.write_text("""
    [
        {
            "apartment": "A1",
            "settlement_year": 2024,
            "settlement_month": 3,
            "amount_pln": 300,
            "type": "rent",
            "date_due": "2024-03-15"
        }
    ]
    """)

    transfers.write_text("""
    [
        {
            "tenant": "Jan",
            "date": "2024-03-05",
            "settlement_year": 2024,
            "settlement_month": 3,
            "amount_pln": 50
        },
        {
            "tenant": "Anna",
            "date": "2024-03-07",
            "settlement_year": 2024,
            "settlement_month": 3,
            "amount_pln": 200
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

    debtors = manager.get_debtors("A1", 3, 2024)

    assert debtors == ["Jan"]
