# Search for next_talk to get to the most recent talks
import argparse
import datetime
import filecmp
import os
import sys

# Disable long line errors thrown by overviews, headlines, etc
# ruff: noqa: E501


class Author:
    def __init__(self, name, affiliation=None):
        self.name = name
        self.affiliation = affiliation


class Talk:
    def __init__(
        self,
        date,
        author,
        *,
        title,
        subtitle=None,
        overview=None,
        categories="",
        headline="",
        attachments=None,
        review=True,
        review_text=None,
    ):
        if len(date) != 10:
            sys.exit("Talk date must be of form 'YYYY-MM-DD'")
        self.date = date
        self.shortdate = date[:-3]
        self.author = author
        self.title = title
        self.subtitle = subtitle
        self.overview = overview
        self.categories = categories
        self.headline = headline
        self.attachments = attachments
        self.review = review
        self.review_text = review_text


previous_talks = [
    Talk(
        "2024-01-22",
        Author("Ian Goodhall"),
        title="The Man Who Caught a Million Criminals",
        subtitle="Invention of DNA Fingerprinting",
        categories="dna",
    ),
    Talk(
        "2024-02-26",
        Author(
            "Professor Jim Smith",
            affiliation="Professor of Environmental Science, School of Environmental, Geographical and Geological Sciences, University of Portsmouth",
        ),
        title="Chernobyl",
        subtitle="Science, Society and Vodka",
        categories="nuclear energy",
    ),
    Talk(
        "2024-03-25",
        Author(
            "Dr Daniela Saadeh",
            affiliation="Research Fellow, Institute of Cosmology and Gravitation, University of Portsmouth",
        ),
        title="Dark Universe",
        subtitle="The invisible majority of the Cosmos",
        categories="space",
    ),
    Talk(
        "2024-04-22",
        Author("Kevin Brown MBE", affiliation="Distinguished Scientist, Elekta"),
        title="Magnetic Resonance Guided Radiotherapy",
        categories="[medicine, health]",
    ),
    Talk(
        "2024-05-20",
        Author(
            "Georgie Banfield",
            affiliation="Research Associate, Insitute of Marine Sciences, University of Portsmouth",
        ),
        title="Competitive Angling as a Scientific Tool",
        subtitle="The CAST Project",
        categories="[environment, citizen science]",
    ),
    Talk(
        "2024-06-24",
        Author(
            "Dr James Kinross",
            affiliation="Senior Lecturer / Consultant Surgeon, Imperial College, London",
        ),
        title="An Internal Climate Crisis",
        subtitle="Lessons From The Microbes That Live Within",
        categories="[medicine, health]",
    ),
    Talk(
        "2024-07-22",
        Author("Dr Tony Whitbread", affiliation="President, Sussex Wildlife Trust"),
        title="There is No Wealth but Life",
        categories="environment",
    ),
    Talk(
        "2024-08-19",
        Author("Keith Herbert", affiliation="Pathfinder Delivery Lead, Southern Water"),
        title="Clean Rivers and Seas",
        categories="environment",
    ),
    Talk(
        "2024-09-23",
        [
            Author(
                "Professor Mike Lauder",
                affiliation="Professor of Sports Biomechanics, Univeristy of Chichester",
            ),
            Author(
                "Professor Sam Blacker",
                affiliation="Professor of Exercise Physiology and Nutrition, Univeristy of Chichester",
            ),
        ],
        title="What is Sports Science?",
        categories="sports science",
    ),
    Talk(
        "2024-10-29",
        Author("Dr Carolyn Cobbold"),
        title="Food to Dye For",
        subtitle="How man-made chemicals became legalised food ingredients",
        categories="[food, chemistry]",
    ),
    Talk(
        "2024-11-25",
        Author("Gary Mason"),
        title="The Wonders of Water",
        categories="[environment, chemistry]",
    ),
    Talk(
        "2024-12-16",
        Author("Robert Hornby"),
        title="The James Webb Telescope",
        categories="space",
    ),
    Talk(
        "2025-01-27",
        Author("Professor Matt Guille", affiliation="University of Portsmouth"),
        title="Clawed Frogs and Medicine",
        subtitle="Pregnancy Testing to Disease Diagnosis",
        overview="""Matt Guille grew up on the Island of Guernsey before his degree and PhD in Biochemistry at King's College London. Post-doctoral research at the Imperial Cancer Research Fund (now the Crick) and the University of London's Developmental Biology Research Centre followed before moving to the Biophysics unit at Portsmouth to start his own lab. During all of this period Matt worked on how genes are controlled and on their functions. In 2006 Matt established the European Xenopus Resource Centre for the research community, it is now the "go to" facility in the world for research using the clawed frogs. Nowadays his research focuses on diagnosis and understanding of rare genetic diseases.

This presentation will start by introducing genes and their function very briefly and then describe why  Xenopus frogs are such powerful "model organisms". followed by what the Resource Centre does. We will then move onto the rare disease programme. Although these are called rare diseases, around 7000 of these have been discovered and 1 in 17 people in the UK has one of these. Recent advances in DNA sequencing and analysis driven by the 100 000 genomes project have allowed the potential disease-causing variations in patient genomes to be identified. Despite this fewer than half of patients have a diagnosis. Five years ago we started to use the tadpole to test the link between potential disease-causing patient gene variants and their disease. We continue to develop this technology but have already identified some 30 new diseases.""",
        categories="[medicine, health]",
    ),
    Talk(
        "2025-02-24",
        Author("Kevin Brown MBE CPhys FlnstP"),
        title="Lowering Our Carbon Footprint",
        subtitle="A Personal Journey",
        overview="""Since moving to Fishbourne, 6 years ago, we have been lowering our Carbon footprint. My talk will cover some interesting things that I have learned on the way. There often seems to be misinformation about these topics in the press and I will explain the science to enable us all to make good decisions. Heat Pumps, are they hype, do they really work and how well? Solar Panels, how much do they help? Home batteries, are they worth the expense? What about Hydrogen? Plus other interesting information. The talk will be about science in a practical setting and I am expecting that it will provoke some lively discussion.""",
        categories="[environment]",
        attachments="""* Kevin's presentation: [Lowering Our Carbon Footprint](resources/2025-02_presentation.pdf){target="_blank"}
* [Protons for Breakfast: Retrofit Journeys](resources/2025-02_retrofit-journeys.pdf){target="_blank"}""",
    ),
    Talk(
        "2025-03-24",
        Author("Dr Ian Goodall"),
        title="The Story of Vaccines",
        subtitle="Edward Jenner to the Covid 19 vaccine",
        overview="""The talk describes the devastating effects of pandemics such as plague, TB and smallpox, prior to the advent of vaccination.
I describe how the remarkable Lady Mary Wortley Montague, wife of the Ambassador to the Ottoman Empire, introduced a process known as variolation, which greatly reduced deaths from smallpox.
Vaccination proper starts with Edward Jenner, who used cowpox to protect people against smallpox, after an outrageous experiment on his gardener’s son!
The star of the talk is Louis Pasteur, who develops vaccines against a variety of diseases.
I explain how the early 20th century saw increasingly widespread outbreaks of polio and how Jonas Salk developed the first vaccine against it.
I finish by describing how mRNA vaccines were developed to fight Covid.""",
        categories="[medicine, health]",
    ),
    Talk(
        "2025-04-28",
        Author(
            "Professor Tom Cherrett",
            affiliation="Professor of Logistics and Transport Management, University of Southampton",
        ),
        title="Drones in Action",
        subtitle="The Scope for Transforming Medical Logistics",
        overview="""Tom Cherrett, Professor of Logistics and Transport Management, University of Southampton,
will give an overview of how drones are being used across a range of industrial sectors, focussing on their scope for assisting medical logistics, using experiences from trials undertaken in the Solent region.""",
        categories="[logistics]",
    ),
    Talk(
        "2025-05-19",
        Author("Dr Tony Whitbread", affiliation="President, Sussex Wildlife Trust"),
        title="The wildlife and wild places of Sussex",
        overview="""The Sussex Wildlife Trust has some 32 nature reserves, home to a large number of interesting, unusual species, and comprised of rich, diverse habitats.  This talk will not only look at these interesting components but will also examine the ecological relations underpinning these places, including their geology, hydrology and climate.  We will start large scale, looking at our place on the globe and indeed in our solar system and then focus down to some familiar, and perhaps not so familiar places in Sussex.""",
        categories="[environment]",
    ),
    Talk(
        "2025-06-23",
        Author(
            "Dr Andrew Gow",
            affiliation="Research Fellow, Institute of Cosmology and Gravitation, University of Portsmouth",
        ),
        title="CANCELLED: A History of the Universe in <<100 Observations",
        overview="""The world we live on is only a tiny part of the vast universe that has existed for nearly 14 billion years! I will present the history of the universe, travelling backwards in time from the present day to the beginning, stopping along the way to visit planets, galaxies, black holes, and the structure of the universe itself.""",
        categories="space",
        review=False,
        headline="Unfortunately Andrew was ill on the day and unable to attend. We will look to reschedule his talk at some point in the future.",
    ),
    Talk(
        "2025-07-28",
        Author("David Widdup, MA (Cantab) Physics, Biochemistry, Computer Science"),
        title="Magnetism",
        overview="""A Whistle Stop tour of the History, Materials and Applications of Magnetic Science from the Bronze Age to the Edge of the Universe (and Beyond).""",
        categories="physics",
    ),
    Talk(
        "2025-08-18",
        Author("Dr Paul Stallard"),
        title="Behind the Streams",
        subtitle="The Technology That Powers Netflix, iPlayer and the Others",
        overview="""In this talk we'll look at some of the key technology behind today's streaming platforms and find out:

- how they deliver very high bandwidth video over limited bandwidth connections
- how they scale to millions of concurrent streams
- how reliability is achieved
- how data, machine learning and AI are used for everything from recommendations to marketing, content buying and ad insertion""",
        attachments="""# Resources

* Paul's presentation (pdf): [Behind the Streams](resources/2025-08_presentation.pdf){target="_blank"}""",
        categories=["TV/media", "computing"],
    ),
    Talk(
        "2025-09-22",
        Author("Robert Hornby"),
        title="The Panama Canal",
        subtitle="The Gateway between Oceans",
        overview="This talk will include how it was started, the dangers for the workers, the incredible machines invented to build the canal, the skill of the surveyors to find the appropriate site for daming the river and finally how locks work. It will also include types of ships that pass through this waterway and what has been done to future proof the canal.",
        categories="transport",
    ),
    Talk(
        "2025-10-27",
        Author("Tony Nordberg"),
        title="A cheaper, quicker, cleaner addition to the UK's Transport Infrastructure",
        overview="This will be a network of one way Eways for lightweight ‘Ecars’ using the margins between the fence-lines either side of major road and rail routes and elevated across open land. For the road sections of door-to-door journeys Ecars would use their internal short-range batteries and when on the Eways will pick up power for recharge and high-speed traction and be automatically controlled.",
        categories=["transport", "environment"],
    ),
]

next_talk = Talk(
    "2025-11-24",
    Author("Dr Tony Mobbs"),
    title="It's computing Jim, but not as we know it",
    subtitle="An introduction to Quantum Computing",
    review_text="Coming soon...",
)

blank_next_talk = Talk(
    "2025-12-15",
    Author("Speaker TBC"),
    title="Details coming soon",
    review_text="Coming soon...",
)

# Author("name", affiliation="affiliation"),


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

    page += (
        f'::: {{.img-float}}\n![](/posters/{talk.shortdate}.jpg){{width=30% style="float: right; margin: 5px;"}}\n:::\n'
    )

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
    for talk in previous_talks:
        page = talkqmd(talk)
        page += postqmd(talk)
        filename = f"previous/{talk.shortdate}.qmd"
        with open(tmpfile, "w") as f:
            f.write(page)
        update_file(filename, tmpfile, args.backup)

    # Generate the next talk page
    page = talkqmd(next_talk)
    filename = "next/next.qmd"
    with open(tmpfile, "w") as f:
        f.write(page)
    update_file(filename, tmpfile, args.backup)


if __name__ == "__main__":
    main()
