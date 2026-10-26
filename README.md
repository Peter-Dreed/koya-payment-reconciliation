# Payment reconciliation

`payments.jsonl` is an export of payment events from a payments provider, one JSON object per line. The reconciliation script is meant to work out how much money was actually collected, but it doesn't work.

Fix it, in Python (`reconcile.py`) or JavaScript (`reconcile.js`), whichever you prefer. When it's right, it prints a code. Paste that code into the application form.

## How the data works

- Each line is one event: `txn_id`, `status` (`success`, `failed` or `pending`), `amount` in naira, `currency`, and `ts` (when it happened, UTC).
- A payment can be attempted more than once. Every attempt has the same `txn_id`. Only the latest attempt for each `txn_id` counts.
- A payment counts as collected only if its latest attempt is `success`.
- The export comes from a production system and isn't perfectly clean. Ignore lines that can't be read, and events without a `txn_id`. Every other event is valid and must be counted correctly.
- `expected.txt` holds the number of successful payments the finance team counted by hand. The script checks itself against it.

## What to submit

1. Fork this repo, fix the script, and commit your fix to your fork.
2. Run it. Paste the code it prints into the form.
3. Paste the link to your fork into the form.

## The fix

The data file was messy, and the old script didn't handle the mess. Four things were fixed in `reconcile.py`:

1. **Broken lines:** a few lines in the file were garbled, and the script crashed on them. Now it skips them.
2. **Missing ID:** a few payments had no ID. Now they're ignored.
3. **Retries:** the same payment can be tried several times. The old script counted every success, so some payments were counted twice. Now it only looks at the last try for each payment. If that last try succeeded, it counts.
4. **Numbers with commas:** some amounts looked like `"4,804.15"`, and the script couldn't read them as numbers. Now it removes the comma first.

After that, the script counts 22,733 successful payments, which matches the finance team's hand count.
