<a href="https://github.com/Pranav-Singh-Devloper">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
    <img alt="Pranav Singh, AI/ML engineer building LLM agents, agent memory and tokenizers from first principles" src="assets/header-light.svg" width="100%">
  </picture>
</a>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500&size=17&duration=2600&pause=1100&color=FF6B5B&center=true&vCenter=true&width=760&height=34&lines=%3E%3E%3E+giving+AI+agents+a+memory+that+knows+when+facts+changed;%3E%3E%3E+writing+tokenizers+from+scratch+until+they+match+GPT-2;%3E%3E%3E+turning+web+research+into+cited+reports%2C+then+posts;%3E%3E%3E+running+the+stats+test+before+believing+the+chart" alt="What I'm working on">
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/pranav-singh-08155a244/"><img src="https://img.shields.io/badge/LinkedIn-14213D?style=flat-square&logo=linkedin&logoColor=F4EDE0" alt="LinkedIn"></a>
  <a href="mailto:pranav.singh2024@nst.rishihood.edu.in"><img src="https://img.shields.io/badge/Email-14213D?style=flat-square&logo=gmail&logoColor=F4EDE0" alt="Email"></a>
  <a href="https://huggingface.co/pranav-singh-developer-1"><img src="https://img.shields.io/badge/Hugging_Face-14213D?style=flat-square&logo=huggingface&logoColor=FFD21E" alt="Hugging Face"></a>
  <a href="https://www.kaggle.com/pranavsinghdeveloper"><img src="https://img.shields.io/badge/Kaggle-14213D?style=flat-square&logo=kaggle&logoColor=20BEFF" alt="Kaggle"></a>
  <a href="https://leetcode.com/u/hawkeye_1/"><img src="https://img.shields.io/badge/LeetCode-14213D?style=flat-square&logo=leetcode&logoColor=FFA116" alt="LeetCode"></a>
  <a href="https://codeforces.com/profile/hawkeye_1"><img src="https://img.shields.io/badge/Codeforces-14213D?style=flat-square&logo=codeforces&logoColor=F4EDE0" alt="Codeforces"></a>
  <a href="https://www.codechef.com/users/hawkeye_1"><img src="https://img.shields.io/badge/CodeChef-14213D?style=flat-square&logo=codechef&logoColor=F4EDE0" alt="CodeChef"></a>
  <img src="https://komarev.com/ghpvc/?username=Pranav-Singh-Devloper&label=profile%20views&color=FF6B5B&style=flat-square" alt="Profile views">
</p>

$$\theta^{\ast}_{\text{pranav}} = \arg\min_{\theta}\ \mathbb{E}_{x\sim\text{real problems}}\left[\mathcal{L}_{\text{shipped}}(x;\theta)\right]$$

<details>
<summary><b>⚡ The 30-second version</b> &nbsp;<sub>(for recruiters)</sub></summary>
<br>

- **Who:** B.Tech CS & AI student at Newton School of Technology (2024–2028). I build LLM systems and test them properly.
- **Built:** [Engram](https://github.com/Pranav-Singh-Devloper/Engram), memory for AI agents that tracks *when* each fact was true; [The Tokenizer](https://github.com/Pranav-Singh-Devloper/The_Tokenizer), three tokenizer families from scratch that match GPT-2 token for token; [Nexus](https://github.com/Pranav-Singh-Devloper/nexus-project), a LangGraph research agent that writes cited reports.
- **Experience:** AI/ML Development Intern at The MA Studio (2025): hybrid BM25 + 70B-LLM retrieval, Streamlit pipelines.
- **Also:** Smart India Hackathon 2024 finalist (top 7) · Secretary, GDG Rishihood · represented Haryana at the National Youth Festival.
- **Looking for:** AI/ML internships and open-source collaborations. [Email me.](mailto:pranav.singh2024@nst.rishihood.edu.in)

</details>

## `model_card.yaml`

<!--CARD:START-->
```yaml
model_id:      pranav-singh/ai-ml-engineer
base_model:    B.Tech CS & AI, Newton School of Technology (2024–2028)
fine_tuned_on:
  - AI/ML intern @ The MA Studio (2025): hybrid BM25 + 70B retrieval
  - agent memory, tokenizers, RAG, graph neural nets, evaluation
capabilities:  [llm-agents, rag, agent-memory, tokenization, gnns, a/b-tests]
languages:     [python, typescript, c++, sql]
evals:
  public_repos:             42
  contributions_last_12mo:  819
  leetcode_contest_rating:  1406
  leetcode_solved:          56
  codeforces_max_rating:    1079
  codechef:                 2★
  smart_india_hackathon:    finalist, top 7 (2024)
known_limitations:
  - rebuilds things from scratch to understand them
  - won't ship a README without a benchmark table
license:       MIT unless the repo says otherwise
last_trained:  2026-11-08  # refreshed daily by a GitHub Action
```
<!--CARD:END-->

## 🧪 Flagship work

<table>
<tr>
<td colspan="2">

<a href="https://huggingface.co/datasets/pranav-singh-developer-1/engram-media/resolve/main/engram-film-1080p.mp4"><img src="assets/cards/engram.jpg" alt="Play the Engram film: the write path, from a chat turn to versioned facts" width="100%"></a>

### [Engram](https://github.com/Pranav-Singh-Devloper/Engram) &nbsp;·&nbsp; memory for AI agents
Agents forget everything between sessions, and similarity search can't tell which of two contradicting messages is current. Engram stores every fact with **two timelines: when it was true, and when it was believed**. It resolves contradictions, forgets what nobody needs and consolidates conversations overnight. Agents use it over **MCP**.

`TypeScript` `Postgres + pgvector` `MCP · 6 tools` `LongMemEval-S` · [**live demo**](https://engram-lime.vercel.app) · [architecture](https://engram-lime.vercel.app/architecture) · [4-min film](https://huggingface.co/datasets/pranav-singh-developer-1/engram-media/resolve/main/engram-film-1080p.mp4)

</td>
</tr>
<tr>
<td width="50%" valign="top">

<a href="https://github.com/Pranav-Singh-Devloper/The_Tokenizer"><img src="assets/cards/tokenizer.jpg" alt="The Tokenizer: BPE training, merge 2" width="100%"></a>

### [The Tokenizer](https://github.com/Pranav-Singh-Devloper/The_Tokenizer)
BPE, byte-level BPE and WordPiece written from scratch in pure Python with zero dependencies, plus an in-browser visualizer that runs the real algorithms step by step.

> **Token-for-token identical to GPT-2** on 338,025 tokens of Shakespeare · 48 + 9 parity tests · 5 experiments

[**live**](https://the-tokenizer.vercel.app) · [2-min explainer](https://huggingface.co/datasets/pranav-singh-developer-1/the-tokenizer-video) (Manim + Remotion)

</td>
<td width="50%" valign="top">

<a href="https://github.com/Pranav-Singh-Devloper/nexus-project"><img src="assets/cards/nexus.jpg" alt="Nexus research dashboard" width="100%"></a>

### [Nexus](https://github.com/Pranav-Singh-Devloper/nexus-project)
Ask a market question. A **LangGraph** agent plans, searches the live web, loops until it can answer, and writes a cited Markdown report. One click turns the report into a LinkedIn post with an AI-generated image.

> Reports searchable **by meaning** (pgvector) · drafts, scheduling and publishing in one place

`React 19` `FastAPI` `LangGraph` `Groq` · [**live**](https://nexus-ai-swarm.vercel.app)

</td>
</tr>
</table>

### 📊 Results table

| project | task | headline result | stack |
|:--|:--|:--|:--|
| [**Traffic Oracle**](https://github.com/Pranav-Singh-Devloper/traffic-oracle) | 5–60 min freeway speed forecasting on METR-LA | I own the deep-learning core: GAT layer, **STGAT**, GRU baseline, trainer · [demo](https://traffic-oracle.streamlit.app/) | PyTorch · graphs |
| [**ML A/B Testing**](https://github.com/Pranav-Singh-Devloper/ml-ab-testing) | LogReg vs RF vs HistGB on 15 OpenML-CC18 datasets | A naive t-test calls RF vs GB "significant" on **11/15** datasets; the 5×2cv test on **1/15**. The test you pick changes the headline. | scikit-learn · stats |
| [**Indian CS Student Survival**](https://github.com/Pranav-Singh-Devloper/indian-cs-student-survival-dataset) | Synthetic dataset for practising classical ML | 10,000 students · 59 features · 7 hidden personas · on [Kaggle](https://www.kaggle.com/datasets/pranavsinghdeveloper/desi-cs-student-survival) and [HF](https://huggingface.co/datasets/pranav-singh-developer-1/indian-cs-student-survival) | pandas · Streamlit |
| [**Viberon**](https://github.com/Pranav-Singh-Devloper/viberon-dmg) | AI dev environment with parallel specialist agents | Agents navigate a **symbol graph** of the codebase instead of reading whole files | TypeScript · agents |
| [**ColdCase RAG**](https://github.com/Pranav-Singh-Devloper/ColdCase_RAG) | Evidence Q&A over case files | Every claim cites a retrieved chunk | FAISS · LangChain · Groq |
| [**Telecom Churn**](https://github.com/Pranav-Singh-Devloper/telecom_churn_prediction) | Churn prediction with explanations | Cost-sensitive threshold (0.3) + SMOTE · [Space](https://huggingface.co/spaces/pranav-singh-developer-1/telecom-churn-predictor) | scikit-learn · Gradio |
| [**RankShift**](https://github.com/Pranav-Singh-Devloper/RankShift-contest-rating-engine) | Contest rating engine | Rating update as a steady-state **Kalman filter** (K = 0.5) · [frontend](https://rank-shift-contest-rating-engine.vercel.app) | TypeScript · Postgres |
| [**Movie Sentiment**](https://github.com/Pranav-Singh-Devloper/movie_sentiment_analysis) | IMDb review classification | 88% accuracy · [Space](https://huggingface.co/spaces/pranav-singh-developer-1/movie-sentiment-analysis) | TensorFlow · Streamlit |

## 📈 Training run

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/generated/training-run-dark.svg">
  <img alt="My GitHub activity as a training run: weekly contributions, streaks, repos and ratings, and my language mix" src="assets/generated/training-run-light.svg" width="100%">
</picture>

<sub>Drawn by <a href="scripts/build_profile.py"><code>scripts/build_profile.py</code></a> (standard-library Python) every day at 00:00 UTC. No third-party stats service, so it doesn't go down.</sub>

### 🚢 Recently shipped
<!--RECENT:START-->
| repo | what | lang | pushed |
|:--|:--|:--|:--|
| [**nexus-project**](https://github.com/Pranav-Singh-Devloper/nexus-project) | Research agent → cited market report → LinkedIn post, end to end | `JavaScript` | today |
| [**the-daily-algorithm**](https://github.com/Pranav-Singh-Devloper/the-daily-algorithm) | The Daily Algorithm — newspaper-editorial AI/ML portfolio of Pranav Singh | `JavaScript` | 4 days ago |
| [**The_Tokenizer**](https://github.com/Pranav-Singh-Devloper/The_Tokenizer) | BPE, byte-level BPE and WordPiece from scratch, GPT-2 parity, live visualizer | `Python` | 5 days ago |
| [**Engram**](https://github.com/Pranav-Singh-Devloper/Engram) | Bitemporal memory for AI agents, served over MCP (Postgres + pgvector) | `TypeScript` | 5 days ago |
| [**ml-ab-testing**](https://github.com/Pranav-Singh-Devloper/ml-ab-testing) | Statistically rigorous A/B test of 3 models on 15 OpenML-CC18 datasets | `Python` | 5 days ago |
<!--RECENT:END-->

## 🏙️ Contribution skyline

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/generated/skyline-dark.svg">
  <img alt="3D skyline of my contribution calendar" src="assets/generated/skyline-light.svg" width="100%">
</picture>

## 🛤️ Trajectory

```mermaid
%%{init: {'theme':'base','themeVariables':{'fontFamily':'ui-sans-serif, system-ui','cScale0':'#14213D','cScaleLabel0':'#F4EDE0','cScale1':'#FF6B5B','cScaleLabel1':'#14213D','cScale2':'#F2B84B','cScaleLabel2':'#14213D'}}}%%
timeline
    2024 : Started B.Tech CS & AI
         : Smart India Hackathon finalist (top 7)
    2025 : AI/ML intern at The MA Studio (hybrid retrieval)
         : Movie sentiment model on HF Spaces
         : Hackathons and RAG systems
    2026 : Traffic Oracle (STGAT on METR-LA)
         : Engram, The Tokenizer, Nexus
         : 10k-student dataset on Kaggle and HF
```

## 🧰 Toolchain

<p>
  <b>ML & data</b><br>
  <img src="https://skillicons.dev/icons?i=py,pytorch,tensorflow,sklearn,opencv,anaconda&theme=dark" alt="Python, PyTorch, TensorFlow, scikit-learn, OpenCV, Anaconda"><br>
  <img src="https://img.shields.io/badge/LangGraph-14213D?style=flat-square&logo=langchain&logoColor=F4EDE0" alt="LangGraph">
  <img src="https://img.shields.io/badge/LangChain-14213D?style=flat-square&logo=langchain&logoColor=F4EDE0" alt="LangChain">
  <img src="https://img.shields.io/badge/Hugging_Face-14213D?style=flat-square&logo=huggingface&logoColor=FFD21E" alt="Hugging Face">
  <img src="https://img.shields.io/badge/pgvector-14213D?style=flat-square&logo=postgresql&logoColor=F4EDE0" alt="pgvector">
  <img src="https://img.shields.io/badge/FAISS-14213D?style=flat-square&logo=meta&logoColor=F4EDE0" alt="FAISS">
  <img src="https://img.shields.io/badge/MCP-14213D?style=flat-square&logo=anthropic&logoColor=F4EDE0" alt="Model Context Protocol">
  <img src="https://img.shields.io/badge/pandas-14213D?style=flat-square&logo=pandas&logoColor=F4EDE0" alt="pandas">
  <img src="https://img.shields.io/badge/NumPy-14213D?style=flat-square&logo=numpy&logoColor=F4EDE0" alt="NumPy">
  <img src="https://img.shields.io/badge/Streamlit-14213D?style=flat-square&logo=streamlit&logoColor=FF6B5B" alt="Streamlit">
  <img src="https://img.shields.io/badge/Gradio-14213D?style=flat-square&logo=gradio&logoColor=F2B84B" alt="Gradio">
</p>
<p>
  <b>Backend & infra</b><br>
  <img src="https://skillicons.dev/icons?i=fastapi,nodejs,express,prisma,postgres,mysql,docker,githubactions,vercel,linux&theme=dark" alt="FastAPI, Node.js, Express, Prisma, Postgres, MySQL, Docker, GitHub Actions, Vercel, Linux">
</p>
<p>
  <b>Frontend & languages</b><br>
  <img src="https://skillicons.dev/icons?i=ts,js,react,nextjs,tailwind,cpp,git&theme=dark" alt="TypeScript, JavaScript, React, Next.js, Tailwind, C++, Git">
</p>

<details>
<summary><b>📄 Full résumé</b></summary>
<br>

**Education**
- **B.Tech, Computer Science & AI** · Newton School of Technology · 2024–2028
- Class XII · Heera Lal Public School · 2023–2024
- Class X · Navy Children School

**Experience**
- **AI/ML Development Intern** · The MA Studio · May–Jun 2025
  - Built a hybrid search-and-retrieval system (BM25 + 70B transformer).
  - Engineered prompt templates and built scalable Streamlit pipelines.

**Leadership & awards**
- Finalist (top 7), Smart India Hackathon 2024
- Secretary, Google Developer Group (GDG), Rishihood University
- Represented Haryana at the National Youth Festival (top 3,000 of 30 lakh)

**Competitive programming:** 250+ problems · LeetCode contest rating 1400+ · CodeChef 2★ · Codeforces max 1079

</details>

---

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/generated/snake-dark.svg">
  <img alt="Snake eating my contribution graph" src="assets/generated/snake.svg" width="100%">
</picture>

<p align="center">
  <sub>The header, training run, skyline and snake are drawn by this repo's own <a href=".github/workflows/refresh-profile.yml">GitHub Action</a>. Fork the setup if you like it.</sub>
</p>
