from __future__ import annotations

import enum
from datetime import date, datetime
from typing import Any

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    type_annotation_map: dict[type[Any], sa.types.TypeEngine[Any]] = {
        datetime: sa.types.TIMESTAMP(timezone=True),
    }

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} n°{self.id} - {self.__str__()}>"


class Techno(enum.StrEnum):
    wind_turbine_onshore = enum.auto()
    wind_turbine_offshore = enum.auto()

    solar_field_ground_mounted = enum.auto()
    solar_field_rooftop = enum.auto()
    solar_field_canopy = enum.auto()

    hydro_turbine_run_of_river = enum.auto()
    hydro_turbine_pumped_storage = enum.auto()
    hydro_turbine_reservoir = enum.auto()

    cogeneration_biomass = enum.auto()
    cogeneration_waste = enum.auto()
    cogeneration_other = enum.auto()


class Site(Base):
    __tablename__ = "sites"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(100), unique=True)
    capacity: Mapped[float] = mapped_column(doc="Installed capacity in [kW]")
    techno: Mapped[Techno] = mapped_column()

    contracts: Mapped[list["Contract"]] = relationship(back_populates="site")

    def __str__(self) -> str:
        return self.name


class Contract(Base):
    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(primary_key=True)
    purchase_order: Mapped[str] = mapped_column(sa.String(50), unique=True)

    start_date: Mapped[date] = mapped_column(sa.Date)
    end_date: Mapped[date] = mapped_column(sa.Date)

    site_id: Mapped[int] = mapped_column(sa.ForeignKey("sites.id"))
    site: Mapped["Site"] = relationship(back_populates="contracts")

    invoices: Mapped[list["Invoice"]] = relationship(back_populates="contract")

    def __str__(self) -> str:
        return self.purchase_order


class InvoiceStatus(enum.StrEnum):
    draft = enum.auto()
    computed = enum.auto()
    error = enum.auto()
    published = enum.auto()
    paid = enum.auto()


class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(primary_key=True)

    publication_id: Mapped[str] = mapped_column(sa.String(50), unique=True)
    issued_at: Mapped[datetime] = mapped_column(server_default=sa.func.now())
    amount: Mapped[float] = mapped_column()

    status: Mapped[InvoiceStatus] = mapped_column()

    contract_id: Mapped[int] = mapped_column(sa.ForeignKey("contracts.id"))
    contract: Mapped["Contract"] = relationship(back_populates="invoices")

    def __str__(self) -> str:
        return f"{self.publication_id} - {self.status}"


mapper_registry = sa.orm.registry()
mapper_registry.update_type_annotation_map(
    {Techno: sa.String, InvoiceStatus: sa.String}
)
