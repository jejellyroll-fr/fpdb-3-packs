# fpdb-3 packs

HUD packages and stat packs for [fpdb-3](https://github.com/jejellyroll-fr/fpdb-3),
shared by its players. fpdb installs them from here with **Tools ▸ Get packs**.

| Pack | Kind | What it is |
| --- | --- | --- |
| FPDB Basic (NLHE 6-max) | HUD | The starter HUD: eight numbers and two popups, native stats only. |
| FPDB Advanced (NLHE 6-max) | HUD | Opens fpdb's popup library: opening by position, 3-bet and 4-bet lines, c-bets by street. |
| FPDB Dynamic (NLHE 6-max) | HUD | Panels that follow the hand: facing an open, a 3-bet, a c-bet, blind defence, short stacks. |
| FPDB Dynamic (PLO 6-max) | HUD | The dynamic HUD for Pot Limit Omaha 6-max. |
| Steals | Stat pack | How often the button and the small blind raise first in. |
| Blind defence | Stat pack | How the big blind answers a single open from the late seats: fold, call or 3-bet. |

## Using a pack

In fpdb, open **Tools ▸ Get packs**, pick a pack and choose **Install**.

- A **HUD** adds its profiles and popups to your HUD configuration. It never
  replaces anything of yours, and does not take over your tables: choose its
  profile for a game in **Preferences ▸ HUD**.
- A **stat pack** adds its stats to the HUD's stat picker and to Research.

Restart fpdb and the HUD afterwards. **Update** and **Uninstall** are in the
same window.

## What a pack can and cannot do

Packs are data. fpdb never runs anything in them:

- a HUD package is an XML layout of stats and popups;
- a stat pack is JSON definitions that can only name metrics, filters and
  fragments fpdb's stat engine already has. It contains no SQL and no code.

Before anything is written, fpdb checks that each package is byte for byte the
one listed in `index.json` (size and SHA-256). It also checks that every stat
and popup the package names exists. A package that fails is refused, and fpdb
says why.

A HUD shows opponents' history. No pack can make fpdb recommend an action.

## Contributing a pack

The quickest way is to let fpdb write it:

1. In fpdb, open **Tools ▸ Share a HUD or pack** (or **Share yours…** in
   **Get packs**). Pick one of your HUD profiles or installed stat packs, give
   it an id (`yourname.topic`), an author, a licence and a description, and
   choose a folder.
2. fpdb writes a folder named after the id, laid out as this repository is. It
   runs the same checks as an install first, so what it writes is accepted
   here. Copy the folder's `hud/`, `stats/` and `sources/` into your copy of
   this repository.
3. Add the content of its `index-entry.json` to the `packs` list of
   `index.json`. Its `sha256` and `size` are already filled in.
4. Optionally add a screenshot in `screens/` and name it in the entry's
   `screenshot`.
5. Open a pull request.

To write a package by hand instead:

1. Add your package:
   - a HUD goes in `hud/<name>.fpdbhud`, which is what fpdb's **Export HUD** writes;
   - a stat pack goes, as its readable folder, in `sources/stats/<your.id>/`,
     with its `manifest.json` (see fpdb's
     [stat pack guide](https://github.com/jejellyroll-fr/fpdb-3/blob/development/docs/stat-packs.md)).
2. Optionally add a screenshot in `screens/`.
3. Add an entry to `index.json`. The fields are described in fpdb's
   [pack gallery guide](https://github.com/jejellyroll-fr/fpdb-3/blob/development/docs/pack-gallery.md).
   - `id` is `yourname.topic`.
   - `license` is required.
   - For a stat pack, `version` must equal its `pack_version`.
4. Run `python scripts/build.py`. It builds the stat pack archives and fills in
   every entry's `sha256` and `size`.
5. Open a pull request. CI runs fpdb's own check on every package
   (`python -m fpdb_3_legacy.pack_gallery validate .`).

A pull request is reviewed before it is merged. A pack that fails the checks,
gives no licence, or is not what its description says is not merged.

## Licence

Each pack carries its own licence, named in `index.json`. The packs published
by the fpdb-3 project are under the GNU Affero General Public License v3.0 or
later, like fpdb-3 itself (`LICENSE`).
