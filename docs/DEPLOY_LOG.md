# FinPilot — Deploy log

*Started 2026-10-21. One entry per deploy that's worth remembering.*

## 2026-10-21 — first public deploy (Phase 2)

**Result:** live at https://finpilot-xsys.onrender.com. The full core loop
(profile → goal → recommendation) was checked end to end on the live site.

**Where it runs:** a free Render Web Service named `finpilot`, built from
this GitHub repo's `main` branch.

| Setting | Value |
| --- | --- |
| Language | Python 3 |
| Build command | `pip install -r requirements.txt` |
| Start command | `uvicorn app:app --host 0.0.0.0 --port $PORT` |
| Instance type | Free (0.1 CPU, 512 MB RAM) |

**What went wrong first, and the fix.** The first deploy built fine but
crashed on start with `Error loading ASGI app. Could not import module
"main"`. The start command said `uvicorn main:app`, but the FastAPI app is
in `app.py`, not `main.py`. Changing the start command to `app:app`
(Settings → Build & Deploy → Start Command) fixed it, and the redeploy
went live.

**Lesson:** in `uvicorn X:Y`, `X` is the Python file name without `.py`
and `Y` is the variable that holds `FastAPI()`. If the log says "Could not
import module", check `X`.

**How it works from now on:**
- Every push to `main` triggers an automatic rebuild and redeploy.
- Free instances sleep after ~15 minutes idle; the first visit afterwards
  takes 30–60 seconds.
- This closes Skill 5 ("how to deploy a small app") from Phase 1, and the
  "running on a deployed URL" part of Phase 2's definition of done.

**Next:** Phase 3 (the interactive simulator). Each phase from here
redeploys the improved version to the same URL.
