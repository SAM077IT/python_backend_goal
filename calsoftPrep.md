Calsoft Interview Preparation Kit
​1. Core Python Fundamentals
​<details>
<summary><b>Q1: What is the Global Interpreter Lock (GIL) in Python?</b></summary>
<p>The GIL is a mutex (lock) that protects access to Python objects, preventing multiple threads from executing Python bytecodes at once. This means multithreading in Python is not truly concurrent for CPU-bound tasks, though it works perfectly fine for I/O-bound tasks. To achieve true parallelism on multi-core machines for CPU-bound tasks, developers use the <code>multiprocessing</code> module instead of <code>threading</code>.</p>
</details>
​<details>
<summary><b>Q2: Explain the difference between lists and tuples.</b></summary>
<p><b>Lists</b> are mutable (can be modified after creation), use square brackets <code>[]</code>, and are slightly slower due to dynamic resizing overhead.

<b>Tuples</b> are immutable (cannot be modified), use parentheses <code>()</code>, and are faster and more memory-efficient. Because they are immutable and hashable, tuples can be used as dictionary keys, whereas lists cannot.</p>
</details>
​<details>
<summary><b>Q3: What are decorators in Python? Provide an example.</b></summary>
<p>Decorators are functions that modify or extend the behavior of another function or class without permanently changing its source code. They are applied using the <code>@</code> symbol syntactic sugar.

<i>Example:</i>

<pre><code>def logging_decorator(func):
def wrapper(*args, **kwargs):
print(f"Calling function: {func.name}")
return func(*args, **kwargs)
return wrapper
​@logging_decorator
def greet(name):
print(f"Hello {name}!")
</code></pre></p>
</details>
​<details>
<summary><b>Q4: How is memory managed in Python?</b></summary>
<p>Python manages memory via a private heap space managed by the Python memory manager. It primarily relies on two mechanisms:

​<b>Reference Counting:</b> Python tracks how many references point to an object. When an object's reference count drops to zero, its memory is immediately freed.

​<b>Garbage Collector:</b> A cyclical garbage collector detects and cleans up "reference cycles" (e.g., Object A points to Object B, and Object B points to Object A, but neither is accessible from the main program).</p>
</details>
​<details>
<summary><b>Q5: What are generators and the <code>yield</code> keyword?</b></summary>
<p>Generators are iterators created using functions that use the <code>yield</code> keyword instead of <code>return</code>. Instead of computing an entire array of values and returning it all at once (which takes up memory), a generator yields values one at a time and pauses its state, making it highly memory-efficient for processing large datasets or streams.</p>
</details>
​2. Django & REST APIs
​<details>
<summary><b>Q1: Explain Django's MVT architecture.</b></summary>
<p>Django follows the Model-View-Template pattern:

​<b>Model:</b> The data layer. It handles database structures, validations, and interactions via Django's Object-Relational Mapping (ORM).

​<b>View:</b> The business logic layer. It receives HTTP requests, queries the Models, processes data, and passes it to the Template or REST framework serializer.

​<b>Template:</b> The presentation layer (HTML/CSS mixed with Django template language).</p>
</details>
​<details>
<summary><b>Q2: What is the difference between <code>select_related</code> and <code>prefetch_related</code>?</b></summary>
<p>- <code>select_related</code>: Used for single-valued relationships (ForeignKey, OneToOne). It performs a SQL <code>JOIN</code> and retrieves the related object in the initial database query.

​<code>prefetch_related</code>: Used for multi-valued relationships (ManyToMany, Reverse ForeignKeys). It performs a separate lookup query for each table and does the "joining" in-memory using Python, preventing the <code>N+1</code> query problem for complex datasets.</p>
</details>
​<details>
<summary><b>Q3: What are Middleware classes in Django?</b></summary>
<p>Middleware is a framework of hooks into Django's request/response processing lifecycle. It acts as a light, low-level plugin system globally altering inputs or outputs. Common examples include <code>AuthenticationMiddleware</code> (associating users with requests), <code>CsrfViewMiddleware</code> (security token checking), and custom logging middleware.</p>
</details>
​<details>
<summary><b>Q4: What are the core HTTP methods used in REST APIs and are they Idempotent?</b></summary>
<p>An operation is idempotent if performing it multiple times yields the same result on the server state.

​<b>GET:</b> Retrieve resource (Idempotent)

​<b>POST:</b> Create new resource (<b>Not</b> idempotent)

​<b>PUT:</b> Update/Replace entire resource (Idempotent)

​<b>PATCH:</b> Partially update resource (Technically non-idempotent, though often treated loosely)

​<b>DELETE:</b> Remove resource (Idempotent)</p>
</details>
​3. Unit Testing Frameworks
​<details>
<summary><b>Q1: Compare <code>unittest</code> and <code>pytest</code>.</b></summary>
<p>- <code>unittest</code>: Built into Python's standard library. It requires boilerplate code, such as writing classes that inherit from <code>unittest.TestCase</code>, and utilizes specific assertions like <code>self.assertEqual()</code>.

​<code>pytest</code>: A highly popular third-party framework. It supports writing tests as simple standalone functions, uses native Python <code>assert</code> statements, and provides a powerful fixture system that simplifies test setup and breakdown.</p>
</details>
​<details>
<summary><b>Q2: What are Pytest Fixtures and how do they help?</b></summary>
<p>Fixtures provide a reliable and repeatable baseline setup for running tests. For example, if multiple tests require a pre-populated database or an API client instance, a fixture can set up that state before the test runs and automatically dismantle or "tear down" the resource after the test finishes using the <code>yield</code> statement.</p>
</details>
​<details>
<summary><b>Q3: What is Mocking and why is it used?</b></summary>
<p>Mocking isolates the specific unit of code being tested by replacing external dependencies (like third-party payment gateways, file structures, or production databases) with simulated mock objects. In Python, this is usually achieved with <code>unittest.mock.patch</code> or the <code>pytest-mock</code> plugin to ensure tests stay fast, deterministic, and isolated from side effects.</p>
</details>
​4. Git Workflows
​<details>
<summary><b>Q1: What is the difference between <code>git merge</code> and <code>git rebase</code>?</b></summary>
<p>- <b>Merge:</b> Combines the history of a source branch into your current branch by creating a dedicated "merge commit". It preserves the true chronological history of both branches exactly as they occurred.

​<b>Rebase:</b> Moves or reapplies a sequence of commits from your current branch on top of a target branch's latest commit. It rewrites project history to yield a completely clean, linear timeline without distracting merge commits.</p>
</details>
​<details>
<summary><b>Q2: How do you resolve a Git merge conflict?</b></summary>
<p>1. Identify the conflicted files using <code>git status</code>.

2. Open those files and locate the conflict markers (<code><<<<<<<</code>, <code>=======</code>, <code>>>>>>>></code>).

3. Manually edit the file contents to choose the desired code combination and delete the marker blocks.

4. Stage the fixed files using <code>git add <filename></code>.

5. Complete the merge or rebase via <code>git commit</code> or <code>git rebase --continue</code>.</p>
</details>
​5. CI/CD Pipelines
​<details>
<summary><b>Q1: Explain the purpose of a CI/CD pipeline.</b></summary>
<p>- <b>Continuous Integration (CI):</b> The practice of frequently pushing code changes to a central repository, which automatically triggers build actions and test execution. It catches bugs and regression bugs quickly.

​<b>Continuous Delivery/Deployment (CD):</b> The automated packaging, staging, and deploying of vetted code to target environments (staging or live production), reducing human error in software releases.</p>
</details>
​<details>
<summary><b>Q2: How do you trigger and structure a GitHub Actions workflow?</b></summary>
<p>GitHub Actions workflows are configured via standard YAML files placed inside the <code>.github/workflows/</code> directory of a repository. They consist of:

​<b>Events:</b> Triggers like <code>push</code> or <code>pull_request</code> on specific branches.

​<b>Jobs:</b> Isolated blocks running on virtual containers/runners (e.g., <code>ubuntu-latest</code>).

​<b>Steps:</b> Sequential tasks execution, running commands (like <code>pip install -r requirements.txt</code>) or predefined community actions (like <code>actions/checkout@v4</code>).</p>
</details>
​6. AI Knowledge (Good-to-Have)
​<details>
<summary><b>Q1: What is Retrieval-Augmented Generation (RAG)?</b></summary>
<p>RAG is an architectural pattern that improves an LLM's accuracy by grounding it on factual external data. When a user submits a query, a backend service first searches a data source (typically a vector database containing custom documents) for contextually relevant information. It then combines the original query with this fetched background context and passes it to the LLM, reducing hallucinations.</p>
</details>
​<details>
<summary><b>Q2: What Python ecosystems are used to manage AI application layers?</b></summary>
<p>Backend developers often use <b>LangChain</b> or <b>LlamaIndex</b> to handle orchestration (chaining prompts, managing state, connecting to databases), <b>OpenAI/Google GenAI SDKs</b> for direct API calls, and frameworks like <b>FastAPI</b> or <b>Django Ninja</b> to wrap these pipelines into scalable, async-capable endpoints.</p>
</details>