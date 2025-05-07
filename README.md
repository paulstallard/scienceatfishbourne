# Science at Fishbourne

## Playbook

### Update after a meeting

Update the local repo

``` bash
git fetch
git pull
```

- Edit `index.qmd`
    - Remove last meeting date from list of next meeting dates
- Edit `scripts/talkpages.py`
    - Move the `Talk` in `next_talk` to the end of `previous_talks` array
    - Add category/categories
    - Add `review="Coming soon...` if not yet available
- Create a new entry for `next_talk`
- If no details available yet:
    - Make new placeholder image (`placeholder_poster`)
        - `cp placeholder.jpg posters/YYYY_MM.qmd`
    - Use `"Details coming soon"` as title
    - Use `"Speaker TBC"` as author
- Run `python scripts/talkpages.py` (or just `make`)

Update remote repo

``` bash
git status
git add .
git commit -m "Update following XXX meeting"
git push
```

### Replace placeholder poster with real poster

- Convert poster to jpg (`convert XXXX posters/YYYY-MM.jpg`).
This will overwrite the placeholder image

### Add review

- Remove the `review="..."` from the Talk object in `talkpages.py`
- Convert the review to markdown and save it to `reviews/_YYYY-MM.qmd`
(if required, use `pandoc review.docx -o reviews/_YYYY_MM.qmd`).
- Run `python scripts/talkpages.py` (or just `make`)
