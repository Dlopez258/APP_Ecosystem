-- =============================================================================
-- BASE DE DATOS: ecosystem_db
-- Proyecto: EcoSystem — Gestión de Residuos Electrónicos (RAEE)
-- Motor: MySQL 8.x
-- Descripción: Esquema unificado que integra el diseño original del proyecto
--              Flask/ORM con los aportes del compañero de equipo.
--              Mantiene compatibilidad total con los modelos SQLAlchemy.
-- =============================================================================

-- Crear la base de datos si no existe y seleccionarla
CREATE DATABASE IF NOT EXISTS ecosystem_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE ecosystem_db;

-- =============================================================================
-- TABLA: usuarios
-- Descripción: Ciudadanos, empresas y gobiernos que usan la plataforma.
-- Cambios integrados del compañero: + telefono, + barrio
-- Columnas propias conservadas: password_hash, tipo_usuario, puntos_acumulados,
--                               activo (necesarias para auth y gamificación)
-- =============================================================================
CREATE TABLE IF NOT EXISTS usuarios (
    id                  INT             NOT NULL AUTO_INCREMENT,
    nombre              VARCHAR(120)    NOT NULL                    COMMENT 'Nombre completo del usuario',
    email               VARCHAR(150)    NOT NULL                    COMMENT 'Correo electrónico único para login',
    password_hash       VARCHAR(256)    NOT NULL                    COMMENT 'Hash Werkzeug de la contraseña',
    tipo_usuario        ENUM(
                            'ciudadano',
                            'empresa',
                            'gobierno'
                        )               NOT NULL DEFAULT 'ciudadano' COMMENT 'Rol del usuario en la plataforma',
    puntos_acumulados   INT             NOT NULL DEFAULT 0          COMMENT 'Puntos de gamificación acumulados',
    ciudad              VARCHAR(100)                                COMMENT 'Ciudad principal de residencia',
    -- Campos integrados del aporte del compañero
    telefono            VARCHAR(20)                                 COMMENT 'Teléfono de contacto (aporte compañero)',
    barrio              VARCHAR(100)                                COMMENT 'Barrio o sector dentro de la ciudad (aporte compañero)',
    -- -----------------------------------------------------------------------
    fecha_registro      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha y hora de registro',
    activo              TINYINT(1)      NOT NULL DEFAULT 1          COMMENT '1=activo, 0=eliminado lógicamente',

    PRIMARY KEY (id),
    UNIQUE KEY uq_usuarios_email (email)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Usuarios del sistema: ciudadanos, empresas y gobiernos';


-- =============================================================================
-- TABLA: puntos_recoleccion
-- Descripción: Centros de acopio donde los ciudadanos entregan dispositivos.
-- Cambios integrados del compañero: + entidad, + fecha_creacion
-- =============================================================================
CREATE TABLE IF NOT EXISTS puntos_recoleccion (
    id                  INT             NOT NULL AUTO_INCREMENT,
    nombre              VARCHAR(150)    NOT NULL                    COMMENT 'Nombre del punto de recolección',
    direccion           VARCHAR(255)    NOT NULL                    COMMENT 'Dirección física del punto',
    ciudad              VARCHAR(100)    NOT NULL                    COMMENT 'Ciudad donde está ubicado',
    latitud             DECIMAL(10,8)                               COMMENT 'Coordenada geográfica latitud',
    longitud            DECIMAL(11,8)                               COMMENT 'Coordenada geográfica longitud',
    horario             VARCHAR(200)                                COMMENT 'Horario de atención (ej: Lun-Vie 8-16)',
    tipos_aceptados     VARCHAR(255)                                COMMENT 'Categorías aceptadas separadas por coma',
    -- Campos integrados del aporte del compañero
    entidad             VARCHAR(120)                                COMMENT 'Entidad responsable: Alcaldía, ONG, empresa privada, etc. (aporte compañero)',
    fecha_creacion      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de registro del punto (aporte compañero)',
    -- -----------------------------------------------------------------------
    activo              TINYINT(1)      NOT NULL DEFAULT 1          COMMENT '1=activo, 0=desactivado lógicamente',

    PRIMARY KEY (id),
    -- Índice para búsquedas rápidas por ciudad (aporte compañero: idx_puntos_municipio)
    INDEX idx_puntos_ciudad (ciudad)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Puntos de recolección / centros de acopio de RAEE';


-- =============================================================================
-- TABLA: dispositivos
-- Descripción: Aparatos eléctricos y electrónicos (RAEE) registrados.
-- Cambios integrados del compañero: + 'tablet' e 'impresora' al ENUM categoria,
--                                   + 'nuevo' e 'irreparable' al ENUM estado
-- Columnas propias conservadas: nombre, usuario_id, fecha_registro
--   (el compañero no tenía dueño del dispositivo ni fecha — necesarios para el ORM)
-- =============================================================================
CREATE TABLE IF NOT EXISTS dispositivos (
    id                  INT             NOT NULL AUTO_INCREMENT,
    nombre              VARCHAR(100)    NOT NULL                    COMMENT 'Nombre descriptivo del dispositivo',
    categoria           ENUM(
                            'celular',
                            'computador',
                            'bateria',
                            'electrodomestico',
                            'tarjeta_madre',
                            'tablet',       -- aporte compañero
                            'impresora',    -- aporte compañero
                            'otro'
                        )               NOT NULL                    COMMENT 'Categoría del dispositivo RAEE',
    marca               VARCHAR(100)                                COMMENT 'Marca del dispositivo',
    estado              ENUM(
                            'nuevo',        -- aporte compañero
                            'funcional',
                            'dañado',
                            'obsoleto',
                            'irreparable'   -- aporte compañero
                        )               NOT NULL                    COMMENT 'Estado físico del dispositivo',
    peso_kg             DECIMAL(6,2)                                COMMENT 'Peso en kilogramos',
    descripcion         TEXT                                        COMMENT 'Descripción adicional del dispositivo',
    -- Relación con el propietario (esencial para el flujo del ORM)
    usuario_id          INT             NOT NULL                    COMMENT 'ID del usuario propietario',
    fecha_registro      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de registro del dispositivo',

    PRIMARY KEY (id),
    CONSTRAINT fk_dispositivos_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Dispositivos electrónicos RAEE registrados por los usuarios';


-- =============================================================================
-- TABLA: entregas
-- Descripción: Registro de cada entrega de dispositivo en un punto de acopio.
-- Cambios integrados del compañero: + cantidad, + observaciones
--                                   + 'verificado', 'en_proceso', 'reutilizado'
--                                     al ENUM estado
-- Columna peso_kg: ya estaba en el compañero Y es útil para estadísticas
--                  del dashboard → se agrega aquí también
-- Columnas propias conservadas: puntos_otorgados, hash_blockchain
-- =============================================================================
CREATE TABLE IF NOT EXISTS entregas (
    id                      INT             NOT NULL AUTO_INCREMENT,
    usuario_id              INT             NOT NULL                COMMENT 'Usuario que realiza la entrega',
    dispositivo_id          INT             NOT NULL                COMMENT 'Dispositivo que se entrega',
    punto_recoleccion_id    INT             NOT NULL                COMMENT 'Punto donde se entrega',
    fecha_entrega           DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha y hora de la entrega',
    estado                  ENUM(
                                'pendiente',
                                'recibido',
                                'verificado',   -- aporte compañero
                                'en_proceso',   -- aporte compañero
                                'procesado',
                                'reutilizado',  -- aporte compañero
                                'reciclado'
                            )               NOT NULL DEFAULT 'pendiente' COMMENT 'Estado del proceso de la entrega',
    puntos_otorgados        INT             NOT NULL DEFAULT 0      COMMENT 'Puntos de gamificación otorgados por esta entrega',
    hash_blockchain         VARCHAR(256)                            COMMENT 'Hash SHA-256 del bloque blockchain asociado',
    -- Campos integrados del aporte del compañero
    cantidad                SMALLINT        NOT NULL DEFAULT 1      COMMENT 'Cantidad de unidades entregadas (aporte compañero)',
    peso_kg                 DECIMAL(6,2)                            COMMENT 'Peso total en kg de los dispositivos entregados (aporte compañero)',
    observaciones           TEXT                                    COMMENT 'Notas adicionales sobre la entrega (aporte compañero)',
    -- -----------------------------------------------------------------------

    PRIMARY KEY (id),
    CONSTRAINT fk_entregas_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_entregas_dispositivo
        FOREIGN KEY (dispositivo_id)
        REFERENCES dispositivos (id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_entregas_punto
        FOREIGN KEY (punto_recoleccion_id)
        REFERENCES puntos_recoleccion (id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    -- Índices para rendimiento (aporte compañero)
    INDEX idx_entregas_usuario  (usuario_id),
    INDEX idx_entregas_punto    (punto_recoleccion_id),
    INDEX idx_entregas_fecha    (fecha_entrega)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Registro de entregas de dispositivos RAEE en puntos de recolección';


-- =============================================================================
-- TABLA: recompensas
-- Descripción: Premios canjeables con los puntos del sistema de gamificación.
-- Sin cambios del compañero (no existía en su esquema — es exclusiva del proyecto)
-- =============================================================================
CREATE TABLE IF NOT EXISTS recompensas (
    id                  INT             NOT NULL AUTO_INCREMENT,
    nombre              VARCHAR(150)    NOT NULL                    COMMENT 'Nombre de la recompensa',
    descripcion         TEXT                                        COMMENT 'Descripción detallada de la recompensa',
    puntos_requeridos   INT             NOT NULL                    COMMENT 'Puntos necesarios para canjear',
    tipo                ENUM(
                            'descuento',
                            'producto',
                            'reconocimiento'
                        )               NOT NULL                    COMMENT 'Tipo de recompensa',
    activo              TINYINT(1)      NOT NULL DEFAULT 1          COMMENT '1=disponible, 0=desactivada',

    PRIMARY KEY (id)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Recompensas del sistema de gamificación canjeables con puntos';


-- =============================================================================
-- TABLA: bloques_blockchain
-- Descripción: Persiste los bloques de la cadena de bloques simulada.
-- Sin cambios del compañero (no existía en su esquema — es exclusiva del proyecto)
-- =============================================================================
CREATE TABLE IF NOT EXISTS bloques_blockchain (
    id                  INT             NOT NULL AUTO_INCREMENT,
    indice              INT             NOT NULL                    COMMENT 'Posición del bloque en la cadena (0 = génesis)',
    timestamp           DATETIME        NOT NULL                    COMMENT 'Fecha y hora de creación del bloque',
    datos               TEXT            NOT NULL                    COMMENT 'JSON con los datos de la entrega trazada',
    hash_previo         VARCHAR(256)    NOT NULL                    COMMENT 'Hash SHA-256 del bloque anterior',
    hash_actual         VARCHAR(256)    NOT NULL                    COMMENT 'Hash SHA-256 de este bloque',
    nonce               INT             NOT NULL DEFAULT 0          COMMENT 'Número usado en la prueba de trabajo',

    PRIMARY KEY (id),
    INDEX idx_blockchain_indice (indice),
    INDEX idx_blockchain_hash   (hash_actual(64))
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Bloques de la cadena de trazabilidad simulada (blockchain educativo)';


-- =============================================================================
-- VISTA: resumen_usuario_entregas
-- Descripción: Muestra el resumen de actividad por usuario.
-- Aporte del compañero: lógica de la vista adaptada a nombres de columnas MySQL.
-- Útil para el dashboard de gobierno y el perfil del ciudadano.
-- =============================================================================
CREATE OR REPLACE VIEW resumen_usuario_entregas AS
SELECT
    u.id                                                AS id_usuario,
    u.nombre,
    u.ciudad,
    u.puntos_acumulados,
    COUNT(e.id)                                         AS total_entregas,
    COALESCE(SUM(e.cantidad), 0)                        AS total_dispositivos,
    ROUND(COALESCE(SUM(e.peso_kg), 0), 2)               AS total_kg,
    MAX(e.fecha_entrega)                                AS ultima_entrega
FROM usuarios u
LEFT JOIN entregas e ON u.id = e.usuario_id
WHERE u.activo = 1
GROUP BY u.id, u.nombre, u.ciudad, u.puntos_acumulados
ORDER BY total_entregas DESC;


-- =============================================================================
-- DATOS INICIALES (SEED)
-- Datos mínimos para poder usar la app inmediatamente.
-- Contraseñas hasheadas con Werkzeug (generate_password_hash):
--   ciudadano@test.com  → password: "ciudadano123"
--   empresa@test.com    → password: "empresa123"
--   gobierno@test.com   → password: "gobierno123"
-- =============================================================================

-- Usuarios de prueba (uno por cada tipo)
INSERT INTO usuarios (nombre, email, password_hash, tipo_usuario, puntos_acumulados, ciudad, telefono, barrio) VALUES
(
    'Carlos Pérez',
    'ciudadano@test.com',
    'scrypt:32768:8:1$salt$hashplaceholder_ciudadano',
    'ciudadano',
    150,
    'Medellín',
    '3001234567',
    'El Poblado'
),
(
    'EcoTech S.A.S.',
    'empresa@test.com',
    'scrypt:32768:8:1$salt$hashplaceholder_empresa',
    'empresa',
    0,
    'Bogotá',
    '6012345678',
    NULL
),
(
    'Alcaldía de Medellín',
    'gobierno@test.com',
    'scrypt:32768:8:1$salt$hashplaceholder_gobierno',
    'gobierno',
    0,
    'Medellín',
    '6044444444',
    NULL
);

-- Puntos de recolección de ejemplo
INSERT INTO puntos_recoleccion (nombre, direccion, ciudad, latitud, longitud, horario, tipos_aceptados, entidad, activo) VALUES
(
    'Punto Verde Mayorca',
    'Centro Comercial Mayorca, Local 215',
    'Sabaneta',
    6.1527,
    -75.6189,
    'Lun-Sáb 10:00-20:00',
    'celular,computador,bateria,tablet',
    'Comfenalco Antioquia',
    1
),
(
    'EcoPunto Alcaldía Medellín',
    'Carrera 52 No. 42-80, Palacio Municipal',
    'Medellín',
    6.2530,
    -75.5688,
    'Lun-Vie 08:00-16:00',
    'celular,computador,bateria,electrodomestico,tarjeta_madre,impresora,otro',
    'Alcaldía de Medellín',
    1
),
(
    'Centro de Acopio EcoTech',
    'Calle 10 No. 43D-55, Zona Industrial',
    'Medellín',
    6.2180,
    -75.5840,
    'Lun-Vie 07:00-17:00, Sáb 08:00-12:00',
    'computador,tarjeta_madre,impresora,electrodomestico',
    'EcoTech S.A.S.',
    1
);

-- Recompensas de ejemplo
INSERT INTO recompensas (nombre, descripcion, puntos_requeridos, tipo, activo) VALUES
(
    'Descuento 10% en Éxito',
    'Cupón de descuento del 10% en cualquier compra en almacenes Éxito.',
    100,
    'descuento',
    1
),
(
    'Bolsa reutilizable EcoSystem',
    'Bolsa ecológica reutilizable con el logo de EcoSystem.',
    200,
    'producto',
    1
),
(
    'Certificado Ciudadano Verde',
    'Certificado digital que reconoce tu compromiso con el reciclaje electrónico.',
    500,
    'reconocimiento',
    1
),
(
    'Descuento 20% Claro Hogar',
    'Descuento del 20% en un mes de servicio de internet Claro.',
    350,
    'descuento',
    1
);

