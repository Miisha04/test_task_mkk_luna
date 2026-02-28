"""init - only seed data

Revision ID: ccc58881e726
Revises: 
Create Date: 2026-02-27 16:55:25.686696

"""
from typing import Sequence, Union
from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'ccc58881e726'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Insert seed data according to technical specification."""

    # ----------------------
    # Buildings
    # ----------------------
    op.execute("""
    INSERT INTO buildings (id, address, coords) VALUES
    (1, 'г. Москва, ул. Ленина 1', ST_GeomFromText('POINT(37.6173 55.7558)', 4326)),
    (2, 'г. Москва, ул. Блюхера 32/1', ST_GeomFromText('POINT(37.6200 55.7520)', 4326)),
    (3, 'г. Москва, ул. Тверская 15', ST_GeomFromText('POINT(37.6050 55.7650)', 4326)),
    (4, 'г. Москва, ул. Арбат 10', ST_GeomFromText('POINT(37.6000 55.7500)', 4326)),
    (5, 'г. Москва, ул. Пушкина 7', ST_GeomFromText('POINT(37.6300 55.7600)', 4326));
    """)

    # ----------------------
    # Activities (3 уровня максимум)
    # ----------------------
    op.execute("""
    INSERT INTO activities (id, name, level, parent_id) VALUES
    -- 1 уровень
    (1, 'Еда', 1, NULL),
    (2, 'Автомобили', 1, NULL),

    -- 2 уровень
    (3, 'Мясная продукция', 2, 1),
    (4, 'Молочная продукция', 2, 1),
    (5, 'Грузовые', 2, 2),
    (6, 'Легковые', 2, 2),

    -- 3 уровень
    (7, 'Запчасти', 3, 6),
    (8, 'Аксессуары', 3, 6);
    """)

    # ----------------------
    # Organizations
    # ----------------------
    op.execute("""
    INSERT INTO organizations (id, name, building_id) VALUES
    (1, 'ООО Рога и Копыта', 1),
    (2, 'Мясной Дом', 2),
    (3, 'АвтоМир', 3),
    (4, 'Truck Service', 4),
    (5, 'Молоко Плюс', 5);
    """)

    # ----------------------
    # Phones (несколько у организации)
    # ----------------------
    op.execute("""
    INSERT INTO phones (id, number, organization_id) VALUES
    (1, '2-222-222', 1),
    (2, '3-333-333', 1),

    (3, '8-923-666-13-13', 2),

    (4, '8-900-111-22-33', 3),
    (5, '8-900-111-22-44', 3),

    (6, '8-800-555-35-35', 4),

    (7, '8-901-777-88-99', 5);
    """)

    # ----------------------
    # Organization <-> Activities
    # ----------------------
    op.execute("""
    INSERT INTO organization_activities (organization_id, activity_id) VALUES
    -- ООО Рога и Копыта занимается всей категорией "Еда"
    (1, 1),

    -- Мясной Дом
    (2, 3),

    -- АвтоМир
    (3, 6),
    (3, 7),

    -- Truck Service
    (4, 5),

    -- Молоко Плюс
    (5, 4);
    """)


def downgrade() -> None:
    pass