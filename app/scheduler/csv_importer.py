import pandas as pd

from app.core.logging import logger
from app.core.normalization import normalize_account_number
from app.models.associate import Associate
from app.repositories.associate_repository import AssociateRepository


class CSVImporter:
    """Import, normalize and persist associate data from a CSV file."""

    def __init__(self):
        self.repository = AssociateRepository()

    async def import_csv(
        self,
        csv_path: str,
    ) -> None:
        logger.info("Reading CSV file")

        df = pd.read_csv(
            csv_path,
            dtype={
                "num_conta": str,
                "num_cpf_cnpj": str,
            },
        )

        logger.info(
            "CSV loaded successfully. Total rows=%s",
            len(df),
        )

        required_columns = {
            "num_conta",
            "nom_associado",
            "num_cpf_cnpj",
            "cod_conglomerado_economico",
        }

        missing_columns = required_columns - set(df.columns)

        if missing_columns:
            logger.error(
                "Missing required columns in CSV: %s",
                sorted(missing_columns),
            )
            raise ValueError(
                f"Missing required columns: {', '.join(sorted(missing_columns))}"
            )

        normalized_df = self.normalize_dataframe(df=df)

        associates = self.create_associates(
            df=normalized_df,
        )

        logger.info(
            "Associate objects created. Total=%s",
            len(associates),
        )

        await self.repository.bulk_upsert(associates=associates)

        logger.info("Associates synchronized successfully.")

    def normalize_dataframe(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        df = df.rename(
            columns={
                "num_conta": "account_number",
                "nom_associado": "name",
                "num_cpf_cnpj": "cpf_cnpj",
                "cod_conglomerado_economico": "economic_group_code",
            }
        )

        df["account_number"] = (
            df["account_number"]
            .astype(str)
            .map(normalize_account_number)
        )

        df["cpf_cnpj"] = (
            df["cpf_cnpj"]
            .astype(str)
            .str.replace(r"\D", "", regex=True)
        )

        df["economic_group_code"] = (
            df["economic_group_code"]
            .astype(int)
        )

        df["name"] = (
            df["name"]
            .str.strip()
        )

        return df

    def create_associates(
        self,
        df: pd.DataFrame,
    ) -> list[Associate]:
        associates = []

        for row in df.itertuples(index=False):
            associate = Associate(
                account_number=row.account_number,
                name=row.name,
                cpf_cnpj=row.cpf_cnpj,
                economic_group_code=row.economic_group_code,
            )

            associates.append(associate)

        return associates
