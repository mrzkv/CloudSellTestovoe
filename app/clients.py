import orjson
from pathlib import Path
from app.models import PricingPlan, Provider
import aiofiles

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

class ProviderClient:
    def __init__(self, provider: Provider, file_name: str):
        self.provider = provider
        self.file_path = DATA_DIR / file_name

    async def get_plans(
            self,
            min_storage: int = 0
    ) -> list[PricingPlan | None]:
        """
        Асинхронно загружаем и фильтруем тарифные планы из JSON-файла.
        :arg min_storage: Минимальный объем хранилища в GB для фильтрации (0 = без фильтрации)
        :return Список отфильтрованных PricingPlan или пустой список при ошибках
        """
        try:
            async with aiofiles.open(self.file_path, 'rb') as f:  # Открываем в бинарном режиме для orjson
                data = await f.read()
                items = orjson.loads(data)

                # Оптимизированное создание и фильтрация за один проход
                return [
                    PricingPlan(
                        provider=self.provider,
                        storage_gb=item["storage_gb"],
                        price_per_gb=item["price_per_gb"]
                    ) for item in items
                    if item["storage_gb"] >= min_storage  # Фильтрация на месте
                ]

        except (FileNotFoundError, orjson.JSONDecodeError, KeyError) as e:
            return []


ProviderClientA = ProviderClient(Provider.A, "provider_a.json")
ProviderClientB = ProviderClient(Provider.B, "provider_b.json")