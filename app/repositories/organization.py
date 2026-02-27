from sqlalchemy import select, union_all, alias
from sqlalchemy.orm import selectinload
from sqlalchemy import cast
from geoalchemy2 import Geography
from sqlalchemy.ext.asyncio import AsyncSession
from geoalchemy2.functions import ST_DWithin, ST_MakePoint, ST_Within, ST_MakeEnvelope, ST_Intersects

from ..models.building import Building
from ..models.organization import Organization
from ..models.activity import Activity, organization_activities

async def get_organizations_by_building(
    db: AsyncSession,
    building_id: int 
) -> list[Organization]:
    result = await db.execute(
        select(Organization)
        .options(
            selectinload(Organization.phones),
            selectinload(Organization.activities),
        )
        .where(Organization.building_id == building_id)
    )

    return result.scalars().all()


async def get_organizations_by_activity_id(
    db: AsyncSession,
    activity_id: int
) -> list[Organization]:
    # рекурсивный CTE: собираем все потомки выбранной активности
    activity_cte = (
        select(Activity.id, Activity.parent_id)
        .where(Activity.id == activity_id)
        .cte(name="activity_cte", recursive=True)
    )

    activity_alias = alias(activity_cte, name="a")
    activity_cte = activity_cte.union_all(
        select(Activity.id, Activity.parent_id)
        .where(Activity.parent_id == activity_alias.c.id)
    )

    # получаем все ID активности (родитель + все потомки)
    activity_ids_stmt = select(activity_cte.c.id)
    result = await db.execute(activity_ids_stmt)
    all_activity_ids = [row[0] for row in result.fetchall()]

    # выбираем организации с любой из этих активностей
    stmt = (
        select(Organization)
        .join(organization_activities)
        .where(organization_activities.c.activity_id.in_(all_activity_ids))
        .options(
            selectinload(Organization.phones),
            selectinload(Organization.activities)
        )
    )

    result = await db.execute(stmt)
    organizations = result.scalars().unique().all()
    return organizations


async def get_organizations_by_activity_name(
    db: AsyncSession,
    activity_name: str
) -> list[Organization]:
    # Сначала находим Activity по имени
    activity_obj_stmt = select(Activity).where(Activity.name == activity_name)
    result = await db.execute(activity_obj_stmt)
    activity_obj = result.scalar_one_or_none()

    if not activity_obj:
        return []  # активности с таким именем нет

    # Рекурсивный CTE для поиска всех потомков выбранной активности
    activity_cte = (
        select(Activity.id, Activity.parent_id)
        .where(Activity.id == activity_obj.id)
        .cte(name="activity_cte", recursive=True)
    )

    activity_alias = alias(activity_cte, name="a")
    activity_cte = activity_cte.union_all(
        select(Activity.id, Activity.parent_id)
        .where(Activity.parent_id == activity_alias.c.id)
    )

    # Получаем все ID активности (родитель + потомки)
    activity_ids_stmt = select(activity_cte.c.id)
    result = await db.execute(activity_ids_stmt)
    all_activity_ids = [row[0] for row in result.fetchall()]

    # Выбираем организации с любой из этих активностей
    stmt = (
        select(Organization)
        .join(organization_activities)
        .where(organization_activities.c.activity_id.in_(all_activity_ids))
        .options(
            selectinload(Organization.phones),
            selectinload(Organization.activities)
        )
    )

    result = await db.execute(stmt)
    organizations = result.scalars().unique().all()
    return organizations


async def get_organization_by_name(
    db: AsyncSession,
    name: str
) -> Organization | None:
    result = await db.execute(
        select(Organization)
        .options(
            selectinload(Organization.phones),
            selectinload(Organization.activities)
        )
        .where(Organization.name == name)
    )

    return result.scalars().one_or_none()


async def get_organization_by_id(
    db: AsyncSession,
    id: int
) -> Organization | None:
    result = await db.execute(
        select(Organization)
        .options(
            selectinload(Organization.phones),
            selectinload(Organization.activities)
        )
        .where(Organization.id == id)
    )

    return result.scalars().one_or_none()


async def get_organizations_in_radius(
    db: AsyncSession,
    radius: int,
    lat: float,
    lon: float,
) -> list[Organization]:
    
    point = ST_MakePoint(lon, lat)

    stmt = (
        select(Organization)
        .join(Organization.building)
        .where(
            ST_DWithin(
                Building.coords,
                point,
                radius
            )
        )
        .options(
            selectinload(Organization.phones),
            selectinload(Organization.activities)
        )
    )

    result = await db.execute(stmt)
    return result.scalars().unique().all()


async def get_organizations_in_square(
    db: AsyncSession,
    min_lat: float,
    min_lon: float,
    max_lat: float,
    max_lon: float,
):
    envelope = cast(
        ST_MakeEnvelope(min_lon, min_lat, max_lon, max_lat, 4326),
        Geography
    )

    stmt = (
        select(Organization)
        .join(Organization.building)
        .where(
            ST_Intersects(Building.coords, envelope)
        )
        .options(
            selectinload(Organization.phones),
            selectinload(Organization.activities)
        )
    )

    result = await db.execute(stmt)
    return result.scalars().unique().all()