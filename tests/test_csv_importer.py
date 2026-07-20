import asyncio

import pandas as pd
import pytest

from app.scheduler.csv_importer import CSVImporter


def test_csv_normalization_uses_expected_field_names_and_digits_only_values():
    df = pd.DataFrame(
        [
            {
                "num_conta": "58151-6",
                "nom_associado": "  Joao Pedro Silva  ",
                "num_cpf_cnpj": "945.449.606-59",
                "cod_conglomerado_economico": "1003",
            }
        ]
    )

    normalized_df = CSVImporter().normalize_dataframe(df)

    assert normalized_df.to_dict("records") == [
        {
            "account_number": "581516",
            "name": "Joao Pedro Silva",
            "cpf_cnpj": "94544960659",
            "economic_group_code": 1003,
        }
    ]


def test_csv_import_fails_when_required_columns_are_missing(tmp_path):
    csv_path = tmp_path / "associates.csv"
    pd.DataFrame(
        [
            {
                "num_conta": "58151-6",
                "nom_associado": "Joao Pedro Silva",
            }
        ]
    ).to_csv(csv_path, index=False)

    with pytest.raises(ValueError, match="Missing required columns"):
        asyncio.run(CSVImporter().import_csv(str(csv_path)))
