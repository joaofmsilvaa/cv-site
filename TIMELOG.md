# Time log

Estimated from file timestamps, server logs and git history (27 Nov 2026, 02:19 – 03:40, plus screenshots at 17:37 and the report). Times are approximate.

| Phase | What | Time spent | Notes / difficulties |
|-------|------|-----------|----------------------|
| 0 | Collect inputs | ~10 min | Data extracted automatically from the existing CV PDF instead of typing it in |
| 1 | CV website | ~25 min | First design rejected and redone (~15 min of this); Playwright had to be installed for screenshots |
| 2 | CMS | ~10 min | Netlify Git Gateway's future unclear, so used Decap's GitHub backend with Netlify OAuth instead |
| 3 | Subdomain + deploy | ~20 min | Commit author had to be corrected (history rewritten + force push); `cd` with backslashes failed in the bash shell; site URL typo (`joaofmsilva` vs `joaofmsilvaa`) fixed |
| 4 | Knowledge pack | ~15 min | CV contained a phone number, so a redacted copy was made; portfolio contradicted the CV (dates, degree name) and was left out as a source |
| 5 | Chatbot creation/training | ~20 min | Free plan limited to 50 message credits/month |
| 6 | Embed chatbot | ~5 min | Netlify's "Powered by Netlify" badge sits under the chat bubble |
| 7 | Conversations | ~15 min | Only a few questions asked to save credits |
| 8 | Report | ~45 min | pandoc not installed; installed a bundled version |
| **Total** | | **~2 h 45 min** | |
