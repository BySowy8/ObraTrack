-- =====================================================================
-- ObraTrack - Esquema SQL para HU2: Registro de imprevistos y retrasos
-- Ejecutar en: Supabase > SQL Editor > New query
-- =====================================================================

-- Extensión necesaria para generar UUIDs automáticamente
create extension if not exists "pgcrypto";

-- ---------------------------------------------------------------------
-- Tabla "obras" (stub mínimo)
-- HU1 (Gestión de Proyectos / Bitácora) probablemente ya va a crear esta
-- tabla con más columnas (dirección, cliente, fechas, etc). La dejamos
-- aquí mínima solo para poder tener la relación (foreign key) desde
-- "imprevistos". Si el compañero de HU1 ya la creó, BORRA este bloque
-- y usa la tabla que él ya tenga.
-- ---------------------------------------------------------------------
create table if not exists obras (
    id          uuid primary key default gen_random_uuid(),
    nombre      text not null,
    creado_en   timestamptz not null default now()
);

-- Fila de prueba para poder probar HU2 sin depender de HU1
insert into obras (nombre)
select 'Obra de prueba - Apartamento 302'
where not exists (select 1 from obras);

-- ---------------------------------------------------------------------
-- Tabla "imprevistos" (el corazón de la HU2)
-- ---------------------------------------------------------------------
create table if not exists imprevistos (
    id               uuid primary key default gen_random_uuid(),
    obra_id          uuid not null references obras(id) on delete cascade,
    fecha            date not null,
    hubo_retraso     boolean not null default false,
    tipo_imprevisto  text not null check (
                        tipo_imprevisto in (
                            'falta_material',
                            'clima',
                            'dano_estructural',
                            'ausencia_personal',
                            'otro'
                        )
                     ),
    descripcion      text not null check (char_length(descripcion) >= 5),
    horas_retraso    numeric(5,2) check (horas_retraso is null or horas_retraso >= 0),
    creado_en        timestamptz not null default now()
);

-- Índices para que la Consulta con Filtrado (HU3) y los filtros de HU2
-- sean rápidos por obra y por fecha.
create index if not exists idx_imprevistos_obra_id on imprevistos(obra_id);
create index if not exists idx_imprevistos_fecha on imprevistos(fecha);

-- ---------------------------------------------------------------------
-- (Opcional pero recomendado) Row Level Security
-- Para el Sprint 1, mientras no haya login todavía, la dejamos abierta
-- con una policy permisiva. Cuando llegue la HU de "Sesión o Control de
-- Acceso" hay que reemplazar esto por policies reales basadas en el rol.
-- ---------------------------------------------------------------------
alter table imprevistos enable row level security;

drop policy if exists "permitir_todo_temporal" on imprevistos;
create policy "permitir_todo_temporal"
    on imprevistos
    for all
    using (true)
    with check (true);
