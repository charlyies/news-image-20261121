# news-image-20261121

![bounty](https://make.fun/badge/news-image-20261121.svg)
![rank](https://make.fun/badge/news-image-20261121/charlyies/news-image-20261121/rank.svg)
![reward](https://make.fun/badge/news-image-20261121/charlyies/news-image-20261121/reward.svg)

A one-image summary of **Saturday 21 November 2026**'s world news, drawn as a
newspaper front page — **THE WORLD TODAY**.

See the bounty: https://make.fun/bounty/news-image-20261121

## What the image sums up

- **Lead — "MISSILES FALL ON POLAND":** two Russian missiles (one a Kh-101
  cruise missile) and a suspected drone came down in south-eastern Poland
  during a mass Russian strike on Ukraine. Warsaw called it a deliberate
  provocation; NATO chief Mark Rutte called it a "grave violation" of Polish
  airspace. No one was hurt.
- **Markets — "WALL STREET SLUMPS":** the S&P 500 slid into correction
  territory as Nvidia plunged about 13% to a 52-week low after Reuters
  reported SEC enforcement staff are examining potential accounting issues
  at the company.
- **Washington — "TRUMP: TAX ON AI CENTRES ABROAD":** the US president said
  American firms building data centres overseas face a ban or a
  "tremendous tax".
- **India — "CYCLONE AKVAN SPARES ODISHA":** 372,000 people were evacuated
  as the cyclone hit the coast near Gopalpur — no deaths and little damage
  reported.
- **Also today:** Myanmar called the ICJ's genocide ruling "unfair", and the
  UK and EU signed food and carbon deals.

## How it is made

The front page is rendered entirely in code with PIL and real fonts
(`compose.py`) — no AI-generated imagery, so every word is spelled
correctly and legible. The lead scene (dusk over Polish farmland, smoke
rising from the impact site, NATO jets overhead) is a layered illustration:
gradient sky, horizon glow, treeline, fields, road, crater and a heavily
blurred smoke plume.

`main.ts` is a Node 22 program (standard library only) that copies
`entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`, validating the PNG
signature, the IHDR dimensions and the 1 MiB / 1024×1024 caps first. It
writes byte-identical output on every run.

## Run it

```sh
python3 compose.py          # re-render entry.png (build time only)
MAKEFUN_OUTPUT_DIR=out node main.ts   # writes out/entry.png
```

## License

MIT — see [LICENSE](LICENSE).
