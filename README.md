# econometrics-book-notebooks

Runnable code-companion notebooks for [simuecon.com](https://simuecon.com) — the
applied analysis pipeline behind each book section (loading data, fitting a model,
interpreting the result), separate from the site's interactive Dash dashboards.

This repo is a **generated mirror** of the notebooks maintained in the private book
repo — don't edit files here directly, changes will be overwritten on the next
publish.

## Structure

Notebooks are organized by language and chapter, mirroring the book itself:

```
{lang}/{chapter_dir}/{section}_notebook.ipynb
{lang}/{chapter_dir}/data/                      # datasets used by that notebook, if any
```

## Running a notebook

- **Colab:** click the "Abrir en Colab" badge at the top of the notebook on the book
  page, or open it directly via
  `https://colab.research.google.com/github/rpasquini/econometrics-book-notebooks/blob/main/<path>`.
- **Locally:** download the `.ipynb` (from the book page or this repo) and open it
  with Jupyter. Data is read directly from this repo's raw GitHub URLs, so no extra
  files need to be downloaded alongside it.
