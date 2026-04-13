from src.manager import Manager
from src.models import Parameters

def test_tenants_total_due_equals_apartment_costs(tmp_path):
    apartments_json = tmp_path / "apartments.json"
    tenants_json = tmp_path / "tenants.json"
    bills_json = tmp_path / "bills.json"
    transfers_json = tmp_path / "transfers.json"

    apartments_json.write_text("""
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

    tenants_json.write_text("""
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

    bills_json.write_text("""
    [
        {
            "apartment": "A1",
            "settlement_year": 2024,
            "settlement_month": 3,
            "amount_pln": 100,
            "type": "utilities",
            "date_due": "2024-03-15"
        },
        {
            "apartment": "A1",
            "settlement_year": 2024,
            "settlement_month": 3,
            "amount_pln": 200,
            "type": "rent",
            "date_due": "2024-03-15"
        }
    ]
    """)

    transfers_json.write_text("[]")

    params = Parameters(
        apartments_json_path=str(apartments_json),
        tenants_json_path=str(tenants_json),
        bills_json_path=str(bills_json),
        transfers_json_path=str(transfers_json)
    )

    manager = Manager(params)

    settlement = manager.get_settlement("A1", 2024, 3)
    assert settlement.total_due_pln == 300

    tenant_settlements = manager.create_tenants_settlements(settlement)
    assert len(tenant_settlements) == 2

    total_tenants_due = sum(ts.total_due_pln for ts in tenant_settlements)

    assert total_tenants_due == settlement.total_due_pln
