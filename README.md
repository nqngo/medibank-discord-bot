# AMIPWNED

Simple bot to grep the Medibank data dumps.

## Prerequisite

- The Medibank data dump.
- `ripgrep`
- Your compression format of choice.
- `python3.10`

## Setup

- Medibank data leak to `/mnt/data`
- Set `DISCORD_TOKEN`
- Set `DISCORD_GUILDS`

## Implementation
This bot uses `ripgrep` as a backend search. On the full data dump (15GB compressed), it takes an average of 300s per query.
It could be done smarter but hey it's not written to be clever. Queries are logged to stdout so optimised as you feel suited.

## Usage
Once add to your discord server: `/amipwned <term> <term2>...`
It is recommended that search term to start with something specific likes email. Each `term` is joined to search inside the line.
