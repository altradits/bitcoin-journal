# bitcoin-journal

My study log for learning Bitcoin from first principles, in public.

## What's here

- **[ROADMAP.md](ROADMAP.md):** the developer track. Twelve exercises, from SHA-256 to Taproot, each built from scratch and checked against a published test vector, ending with a first real pull request to an open-source Bitcoin project.
- **[exercises/](exercises/):** one folder per exercise, with a test in each language (Go, Python, Rust, C++, JavaScript). An exercise counts as done only when its tests pass.
- **[drill-log/](drill-log/):** dated logs of my daily question drills, one line per answer, pass or fail.
- **[curriculum/](curriculum/):** the question bank the drills use, based on [Learn Me A Bitcoin](https://learnmeabitcoin.com).

## Status

| # | Exercise | Status |
|---|---|---|
| 01 | Hashing: SHA-256 and double SHA-256 from scratch | Set up, in progress |
| 02–12 | Base58Check to a first real PR | Not started |

## Run it

```sh
python3 ex.py start 01 go --repo ~/bitcoin-journal   # set up an exercise in a language
python3 ex.py check 01 go --repo ~/bitcoin-journal   # run its tests
```

Part of my [Builder Path](https://altradits.com/tracker) toward full-time open-source Bitcoin work.
