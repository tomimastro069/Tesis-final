# 📦 Comandos rápidos (Docker + DB)
Guía corta para usar el flujo habitual del proyecto con base de datos en Docker.

## 1) Levantar todo

```bash
docker compose up -d --build
```

Levanta: `app` + `zap` + `dvwa` + `db` (PostgreSQL).

## 2) Entrar al contenedor de la app

```bash
docker exec -it security-app sh
```

## 3) Ejecutar el orquestador

```bash
python main.py
```

## 4) Ver logs de servicios

```bash
docker compose logs -f app
docker compose logs -f db
docker compose logs -f zap
docker compose logs -f dvwa
```

## 5) Verificar que Postgres está guardando historial

### Contar registros en `ffuf_history`

```bash
docker exec -it security-db psql -U security_user -d security_history -c "SELECT COUNT(*) FROM ffuf_history;"
```

### Ver últimas filas

```bash
docker exec -it security-db psql -U security_user -d security_history -c "SELECT id, target_url, word, timestamp FROM ffuf_history ORDER BY id DESC LIMIT 20;"
```

## 6) Reiniciar servicios

```bash
docker compose restart
```

O solo uno:

```bash
docker compose restart app
docker compose restart db
```

## 7) Bajar todo

```bash
docker compose down
```

## 8) Bajar todo y borrar volumen de DB (reset total)

```bash
docker compose down -v
```

> ⚠️ Esto elimina los datos persistidos de PostgreSQL.
