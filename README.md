\# 🤖 OrbitDesk Support Agent
## 🌐 Live Demo

🚀 **Try OrbitDesk Support Agent:**
https://orbitdesk-support-agent-hsmgzuh6c4y5w9y5h6exk7.streamlit.app/


An AI-powered support assistant that answers OrbitDesk questions using \*\*Retrieval-Augmented Generation (RAG)\*\* and a pre-trained \*\*LLM\*\*.



\## 📌 Overview



The system uses the provided OrbitDesk knowledge base to answer support questions.



\### 🔄 Workflow



```text

User Question

&#x20;     ↓

🔍 Question Classification

&#x20;     ↓

📚 Retrieve Relevant Knowledge

&#x20;     ↓

📝 Retrieved Evidence

&#x20;     ↓

🤖 LLM through Groq API

&#x20;     ↓

💬 Final Answer

```



\### 🏷️ Question Classification



Questions are classified into three categories:



\* ✅ \*\*ANSWERABLE\*\* — Can be answered using the OrbitDesk knowledge base.

\* ❓ \*\*CLARIFICATION\*\* — More information is needed.

\* 🚫 \*\*NOT\_ANSWERABLE\*\* — Outside the supported OrbitDesk knowledge base.



\## 🧠 RAG Pipeline



RAG combines \*\*retrieval\*\* and \*\*generation\*\*.



1\. 📂 Load the knowledge-base documents.

2\. ✂️ Split documents into smaller chunks.

3\. 🔎 Retrieve the most relevant chunks for the user's question.

4\. 📖 Provide the retrieved evidence to the LLM.

5\. 💬 Generate a natural-language answer based on the evidence.



The LLM is \*\*not trained on the OrbitDesk documents\*\*. The relevant documentation is provided as context when answering each question.



\## 📁 Project Structure



```text

orbitdesk-support-agent/

│

├── data/

│   └── knowledge\_base/

│       ├── 01\_product\_overview.md

│       ├── 02\_roles\_and\_permissions.md

│       ├── 03\_workspace\_settings\_and\_timezones.md

│       ├── 04\_scheduled\_exports.md

│       ├── 05\_api\_credentials.md

│       ├── 06\_connections\_and\_refreshes.md

│       ├── 07\_delivery\_destinations.md

│       ├── 08\_escalation\_and\_diagnostics.md

│       ├── 09\_audit\_logs.md

│       └── 10\_security\_and\_safe\_responses.md

│

├── src/

│   └── orbitdesk/

│       ├── loader.py

│       ├── chunker.py

│       ├── classifier.py

│       ├── retriever.py

│       ├── llm.py

│       └── pipeline.py

│

├── tests/

├── .gitignore

└── README.md

```



\## 🛠️ Main Components



| File            | Purpose                                       |

| --------------- | --------------------------------------------- |

| `loader.py`     | 📂 Loads knowledge-base documents             |

| `chunker.py`    | ✂️ Splits documents into smaller chunks       |

| `classifier.py` | 🏷️ Classifies user questions                 |

| `retriever.py`  | 🔎 Retrieves relevant knowledge-base evidence |

| `llm.py`        | 🤖 Generates answers using the Groq LLM       |

| `pipeline.py`   | 🔗 Connects the complete workflow             |



\## 💻 Technologies



\* 🐍 Python

\* 🧠 RAG

\* 🔤 Sentence Transformers

\* 🤗 Hugging Face

\* ⚡ Groq API

\* 🤖 Llama 3.1 8B Instant

\* 🐙 Git \& GitHub



\## ⚙️ Setup



Create a virtual environment:



```bash

python -m venv .venv

```



Activate it:



```bash

.venv\\Scripts\\activate

```



Install the required dependencies.



Create a `.env` file in the project root:



```text

GROQ\_API\_KEY=your\_api\_key

```



🔒 The `.env` file is excluded from Git using `.gitignore`.



\## ▶️ Run the Project



From the project root:



```bash

python src/orbitdesk/pipeline.py

```



The application returns:



\* 🏷️ Question classification

\* 💬 Generated answer

\* 📚 Retrieved knowledge-base evidence



\## 🧪 Example



\*\*Question:\*\*



```text

Who can create an API credential?

```



\*\*Classification:\*\*



```text

ANSWERABLE

```



\*\*Relevant Evidence:\*\*



```text

KB-005 - API Credentials

```



\*\*Generated Answer:\*\*



```text

Only Owners and Admins can create API credentials.

```



\## 🔐 Security



The application does not request or expose:



\* 🔑 Passwords

\* 🔐 API secrets

\* 🔒 OAuth tokens

\* 🍪 Session cookies

\* 💳 Payment-card information



API credentials are stored in environment variables and are \*\*not committed to GitHub\*\*.



\## ✅ Project Status



The core \*\*RAG pipeline, question classification, evidence retrieval, LLM answer generation, and security handling\*\* have been implemented and tested.



🎉 \*\*Project completed successfully!\*\*



