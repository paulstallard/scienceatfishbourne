# Search for next_talk to get to the most recent talks
import argparse
import datetime
import filecmp
import os

from talk import Author, Talk
from talk_data import LAST_MEETING, science_talks


def gettitle(talk):
    title = f'"{talk.title}"' if ":" in talk.title else talk.title
    if talk.subtitle:
        return f"{title}\nsubtitle: {talk.subtitle}"
    return title


def authlist(authors):
    names = [a.name for a in authors]
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]} and {names[1]}"
    namestr = ", ".join(names[:-1])
    return f"{namestr} and {names[-1]}"


def getauthor(author):
    block = ""
    authors = (author,) if type(author) is Author else author
    for a in authors:
        block += f"  - name: {a.name}\n"
        if a.affiliation:
            block += f"    affiliation: {a.affiliation}\n"
    block += f"author: {authlist(authors)}"
    return block


def header(talk: Talk):
    head = f"---\ntitle: {gettitle(talk)}\n"
    head += f"date: {talk.date}\n"
    head += "authors:\n"
    head += f"{getauthor(talk.author)}\n"
    if talk.categories:
        head += f"categories: {talk.categories}\n"
    return f"{head}---\n\n"


def talkqmd(talk: Talk):
    """Generate the common (top) of the post. Used for both next and previous talks"""
    page = header(talk)
    if talk.headline:
        page += f"{talk.headline}\n\n"

    talktitle = f"{talk.title}: {talk.subtitle}" if talk.subtitle else talk.title
    poster_url = f"/posters/{talk.shortdate}.jpg"
    poster_alttext = f'fig-alt="Poster image for talk entitled {talktitle}"'
    poster_style = 'style="float: right; margin: 5px;"'
    page += f"::: {{.img-float}}\n![]({poster_url}){{width=30% {poster_alttext} {poster_style}}}\n:::\n"

    if talk.overview:
        page += f"\n# Overview\n\n{talk.overview}\n"

    return page


def postqmd(talk: Talk):
    """Generate the post-talk markdown, used only for talks that have already happened"""
    post = f"\n{talk.attachments}\n" if talk.attachments else ""
    if talk.review:
        review = talk.review_text or f"{{{{< include /reviews/_{talk.shortdate}.qmd >}}}}"
        post += f"\n# Lynn's Review\n\n{review}\n"
    return post


def update_file(oldfile, newfile, backup=True):
    if os.path.isfile(oldfile):
        if filecmp.cmp(oldfile, newfile, shallow=False):
            print(f"{oldfile} already up to date")
            os.remove(newfile)
        else:
            if backup:
                ts = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H-%M-%SZ")
                os.rename(oldfile, f"{oldfile}.{ts}")
            os.rename(newfile, oldfile)
            print(f"{oldfile} updated")
    else:
        os.rename(newfile, oldfile)
        print(f"{oldfile} created")


def main():
    parser = argparse.ArgumentParser(description="Generate Talk Pages")
    parser.add_argument("-b", "--backup", action="store_true", help="Backup old version if overwriting")
    args = parser.parse_args()

    tmpfile = "___tmpqmd_23234"
    for talk in science_talks:
        if datetime.date.fromisoformat(talk.date) > LAST_MEETING:
            # Generate the next talk page
            page = talkqmd(talk)
            filename = "next/next.qmd"
            with open(tmpfile, "w") as f:
                f.write(page)
            update_file(filename, tmpfile, args.backup)
            break
        page = talkqmd(talk)
        page += postqmd(talk)
        filename = f"previous/{talk.shortdate}.qmd"
        with open(tmpfile, "w") as f:
            f.write(page)
        update_file(filename, tmpfile, args.backup)


if __name__ == "__main__":
    main()
