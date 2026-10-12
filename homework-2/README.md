# Homework 2: Building a Wikipedia Agent

An agent that searches Wikipedia and reads page content to answer questions about any topic.

- **Framework:** PydanticAI
- **LLM provider:** OpenAI (`gpt-4o-mini`)

## Setup

```bash
cd homework-2
uv sync
cp .env.example .env   # then add your OpenAI key
```

## Files

| File | What it does |
| --- | --- |
| `tools.py` | `search_wikipedia(query)` calls the Search API, `get_page(title)` fetches a page's raw wikitext. Both send the required User-Agent header |
| `agent.py` | PydanticAI agent with both tools; prints each tool call, the answer and the token usage |

```bash
uv run python agent.py "What are the main threats to capybara populations?"
```

## Answers

| # | Question | Answer |
| --- | --- | --- |
| 1 | Results for "capybara" | 10 |
| 2 | Titles containing "capybara" | 6 |
| 3 | Characters in the Capybara page | ~45,000 (44,767) |
| 4 | Framework and provider | PydanticAI + OpenAI (`gpt-4o-mini`) |
| 5 | What the Capybara page is about | See below |
| 6 | Tool calls for the threats question | 3 |

### Q5. Single page

The agent went straight to `get_page("Capybara")` and summarised it:

> The page is about the capybara (*Hydrochoerus hydrochaeris*), the largest living rodent. It's a semi-aquatic herbivore native to South America (everywhere except Chile), living near rivers, lakes and wetlands. The article covers its taxonomy, physical description, grass diet, social groups, reproduction, conservation status (not threatened) and cultural importance.

### Q6. Search then fetch

Tools used, in order:

1. `search_wikipedia("Threats to capybara populations")`
2. `search_wikipedia("Capybara")`
3. `get_page("Capybara")`

Final answer:

> The main threats to capybara populations include:
> 1. **Hunting**: for meat, pelts and grease, causing local declines even though the species isn't globally endangered.
> 2. **Habitat loss**: agriculture and urbanisation degrade the wetlands and grasslands capybaras rely on.
> 3. **Human–wildlife conflict**: farmers see them as competing with livestock for grazing, which leads to intentional killings.
> 4. **Predation**: jaguars, caimans and anacondas, especially of young capybaras.
> 5. **Environmental changes**: climate change altering their habitat and food sources.
>
> Capybaras adapt well to some human-altered environments, and some farming practices help preserve their habitat.

The Wikipedia article itself mainly names hunting and habitat loss; points 3 and 5 look like the model adding general knowledge on top of the page.
