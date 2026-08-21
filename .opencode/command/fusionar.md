---
description: Fusion guiada de una rama hacia master de tu fork (menu interactivo con verificaciones).
agent: guardian-git
---

Ejecuta el "Flujo de fusion a master (con menu)" definido en tu prompt,
para fusionar la rama indicada en master del fork de Hector
(HectorOrlando/youtube-transcript-api). Nunca contra upstream.

Rama objetivo: $ARGUMENTS

Si $ARGUMENTS viene vacio, usa la rama actual (`git branch --show-current`);
si esa rama resulta ser master, pide a Hector el nombre de la rama antes de
continuar. Respeta las verificaciones previas y los menus numerados tal cual
estan definidos; no ejecutes nada destructivo sin su confirmacion explicita.
