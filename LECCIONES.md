# LECCIONES APRENDIDAS (git / GitHub)

Base de conocimiento personal de problemas reales que me han pasado con git
y GitHub en este repositorio, para no repetirlos y para dar contexto rapido
a cualquier IA o persona que trabaje aqui.

Cada leccion tiene: fecha, gravedad, que paso, por que pasa, como detectarlo,
como se soluciono y la regla de oro que dejarla clara.

---

## Indice

1. [El Pull Request se fue al repositorio equivocado](#1-el-pull-request-se-fue-al-repositorio-equivocado)

---

## 1. El Pull Request se fue al repositorio equivocado

**Fecha:** 2026-08-21
**Gravedad:** baja (se detecto a tiempo y no llego a fusionarse)

### Que paso

- Hice commit de mi trabajo en una rama de MI fork
  (`HectorOrlando/youtube-transcript-api`)
- Fui a crear un Pull Request desde la web de GitHub
- Sin darme cuenta, el PR quedo dirigido al repositorio ORIGINAL del autor:
  `jdepoix/youtube-transcript-api` (abrio el PR #615 alli)
- Lo que yo queria era un PR dentro de MI propio fork para fusionar
  mi rama con mi `master`

### Por que pasa

- Cuando trabajas desde un fork, GitHub abre el formulario del PR apuntando
  POR DEFECTO al repositorio upstream (el original), porque esa es la
  configuracion tipica para CONTRIBUIR mejoras al autor
- El formulario tiene 4 selectores arriba y es facil no mirarlos:

```
base repository: jdepoix/youtube-transcript-api        ← destino (EL ERROR ESTABA AQUI)
base: master
head repository: HectorOrlando/youtube-transcript-api  ← origen (mi rama)
compare: 01-mi-rama-de-trabajo
```

### Como detectarlo ANTES de crear el PR

Mirar siempre el selector `base repository`, arriba a la izquierda del
formulario:

| Si dice... | Significa | Que hacer |
|---|---|---|
| `HectorOrlando/...` | El PR queda en MI fork | Correcto, continuar |
| `jdepoix/...` | El PR se propone al AUTOR original | Cambiar el destino (enlace "compare across forks" o desplegable) o cancelar |

### Como se soluciono

```
1. Cerrar el PR equivocado con mensaje cortes:
   gh pr close 615 --repo jdepoix/youtube-transcript-api --comment "Closing this pull request - it was opened by mistake..."

2. Crear de nuevo el PR verificando base repository = HectorOrlando/...
   → Quedo como PR #1 DENTRO de mi propio fork

3. Merge del PR #1 hacia mi master y pull local:
   git checkout master
   git pull origin master
```

Resultado final correcto: los cambios fusionados en `master` de MI fork.
El repo de jdepoix no recibio nada (un PR cerrado nunca fusiona codigo).

### Regla de oro

- `commit` y `merge` = solo LOCAL, nada sale de tu PC
- `push` = sube al remoto QUE TU INDIQUES (`origin` = mi fork, `upstream` = el del autor)
- Un **Pull Request** viaja al repo escrito en `base repository`: ese campo
  manda. Revisalo siempre antes de pulsar "Create pull request"

---
