"""
Configuration settings for IELTS Data Pipeline
"""
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

LISTENING_DIR = DATA_DIR / "listening"
READING_DIR = DATA_DIR / "reading"
WRITING_DIR = DATA_DIR / "writing"
MANIFEST_FILE = DATA_DIR / "manifest.json"

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

FEEDS = {
    "listening": {
        "bbc_6min": "https://podcasts.files.bbci.co.uk/p02pc9tn.rss",
    },
    "reading": {
        "scientific_american": "http://rss.sciam.com/ScientificAmerican-Global",
        "guardian_science": "https://www.theguardian.com/science/rss",
        "guardian_environment": "https://www.theguardian.com/environment/rss",
        "bbc_science": "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml"
    }
}

AWL_WORDS = {
    "analyse": "examine in detail to discover meaning or essential features",
    "approach": "a way of dealing with a situation or problem",
    "assess": "evaluate or estimate the nature, ability, or quality of",
    "assume": "suppose to be the case, without proof",
    "authority": "the power or right to give orders, make decisions, and enforce obedience",
    "available": "able to be used or obtained; at someone's disposal",
    "benefit": "an advantage or profit gained from something",
    "concept": "an abstract idea; a general notion",
    "consistent": "acting or done in the same way over time, especially so as to be fair or accurate",
    "constitute": "be (a part) of a whole; combine to form",
    "context": "the circumstances that form the setting for an event, statement, or idea",
    "criteria": "a principle or standard by which something may be judged or decided",
    "crucial": "decisive or critical, especially in the success or failure of something",
    "derive": "obtain something from a specified source",
    "distribute": "give shares of something; deal out",
    "economic": "relating to the production, consumption, and transfer of wealth",
    "environment": "the surroundings or conditions in which a person, animal, or plant lives",
    "establish": "set up on a firm or permanent basis",
    "estimate": "roughly calculate or judge the value, number, quantity, or extent of",
    "evident": "plain or obvious; clearly seen or understood",
    "factor": "a circumstance, fact, or influence that contributes to a result",
    "function": "an activity that is natural to or the purpose of a person or thing",
    "indicate": "point out; show; suggest as a desirable or necessary course of action",
    "individual": "single; separate; characteristic of a particular person or thing",
    "interpret": "explain the meaning of information or actions",
    "involve": "have or include something as a necessary part or result",
    "issue": "an important topic or problem for debate or discussion",
    "major": "important, serious, or significant",
    "method": "a particular procedure for accomplishing or approaching something",
    "occur": "happen; take place; exist or be found to be present in",
    "period": "a length or portion of time",
    "policy": "a course or principle of action adopted or proposed by an organization",
    "principle": "a fundamental truth or proposition that serves as the foundation",
    "procedure": "an established or official way of doing something",
    "process": "a series of actions or steps taken in order to achieve a particular end",
    "require": "need for a particular purpose; cause to be necessary",
    "research": "the systematic investigation into and study of materials and sources",
    "respond": "say something in reply; react quickly or favorably",
    "role": "an actor's part in a play, film, etc.; the function assumed or part played",
    "section": "any of the more or less distinct parts into which something is divided",
    "significant": "sufficiently great or important to be worthy of attention; noteworthy",
    "similar": "resembling without being identical",
    "source": "a place, person, or thing from which something originates or can be obtained",
    "specific": "clearly defined or identified; precise and clear in statement",
    "structure": "the arrangement of and relations between the parts or elements of something",
    "theory": "a supposition or a system of ideas intended to explain something",
    "vary": "differ in size, amount, degree, or nature from something else of the same type"
}
