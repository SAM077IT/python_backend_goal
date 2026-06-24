​1. Core Python (Advanced & Under-the-Hood)
​<details>
<summary><b>Q6: What is the difference between <code>new</code> and <code>init</code>?</b></summary>
<p>
​<code>new</code> is the actual creator method that allocates memory for the object. It is a static method that returns a new instance of the class.

​<code>init</code> is the initializer method. It receives the instance created by <code>new</code> and sets up attributes. You overwrite <code>new</code> when customizing subclass immutable types or implementing Singleton patterns.
</p>
</details>
​<details>
<summary><b>Q7: What are <code>*args</code> and <code>**kwargs</code>, and how do they impact memory/performance?</b></summary>
<p>
They allow functions to accept a variable number of arguments. <code>*args</code> packages positional arguments into a <b>tuple</b>, while <code>**kwargs</code> packages keyword arguments into a <b>dictionary</b>. Unpacking large sets of arguments can introduce minimal processing overhead, but provides significant flexibility for dynamic decorators or wrappers.
</p>
</details>
​<details>
<summary><b>Q8: Explain the difference between Deep Copy and Shallow Copy.</b></summary>
<p>
​<b>Shallow Copy</b> (<code>copy.copy()</code>): Creates a new collection object, but populates it with references to the child objects found in the original. Altering a nested list inside the copy updates the original.

​<b>Deep Copy</b> (<code>copy.deepcopy()</code>): Recursively copies everything, cloning both the container and its elements. The two structures share zero references.
</p>
</details>
​<details>
<summary><b>Q9: How do Metaclasses work in Python?</b></summary>
<p>
A metaclass is "the class of a class." While standard classes define how instances behave, metaclasses define how standard classes themselves behave. They intercept class creation, allowing you to modify fields, enforce APIs, or automatically register plugins during module load times (Django uses metaclasses extensively under the hood to build database Models).
</p>
</details>
​<details>
<summary><b>Q10: What are slots (<code>slots</code>) used for?</b></summary>
<p>
By default, Python instances store attributes in a dynamic dictionary (<code>dict</code>), which takes up a lot of memory space. Declaring <code>slots</code> optimization allocates a fixed array of attributes instead. It restricts dynamic creation of arbitrary attributes but drastically optimizes RAM utilization when instantiating millions of small objects.
</p>
</details>
​2. Django & REST APIs (Production-Scale Optimization)
​<details>
<summary><b>Q6: What are Django Signals, and when should you avoid them?</b></summary>
<p>
Signals allow decoupled applications to get notified when actions occur elsewhere (e.g., <code>post_save</code> or <code>pre_delete</code>). However, they can make code flows opaque, create invisible side effects, and do <b>not</b> trigger during bulk operations like <code>update()</code> or <code>bulk_create()</code>. Use them sparingly; clear methods on service layers are often preferred.
</p>
</details>  
​<details>
<summary><b>Q7: How do you handle database connection pooling in Django?</b></summary>
<p>
Django establishes a new database connection for each request cycle by default and closes it when done. For heavy scaling, you should set the <code>CONN_MAX_AGE</code> configuration variable in <code>settings.py</code> to reuse persistent connections over multiple incoming requests, or use a dedicated database proxy like PgBouncer.
</p>
</details>
​<details>
<summary><b>Q8: What are Django QuerySet evaluations and how can they cause latency?</b></summary>
<p>
QuerySets are lazy—defining a query doesn't hit the database. It evaluates only when you loop through it, print it, or slice it. Compiling multiple filters in a loop can cause repetitive queries. For optimization, evaluate QuerySets explicitly or use aggregates (<code>Max</code>, <code>Sum</code>) directly inside the database engine.
</p>
</details>  
​<details>
<summary><b>Q9: Explain the difference between Serializer and ModelSerializer in DRF.</b></summary>
<p>
​<code>Serializer</code>: Requires explicit definitions for fields and validation logic, providing complete granular control over non-model payloads.

​<code>ModelSerializer</code>: Automatically inspects a designated Django Model to construct fields, standard model validators, and basic <code>create()</code> / <code>update()</code> implementations natively.
</p>
</details>
​<details>
<summary><b>Q10: How do you mitigate Cross-Site Scripting (XSS) and SQL Injection in Django?</b></summary>
<p>
​Django’s template engine automatically escapes variables containing HTML tags to stop XSS.

​Django’s ORM constructs parameterized raw SQL queries automatically behind the scenes. As long as you don't execute raw strings manually via raw string concentration inside <code>extra()</code> or <code>RawSQL</code> methods, you are safe from SQL injection attacks.
</p>
</details>
​3. Unit Testing (Advanced Framework Concepts)
​<details>
<summary><b>Q5: What is the difference between a Unit Test and an Integration Test?</b></summary>
<p>
​<b>Unit Test:</b> Isolates and verifies small functions or blocks of pure logic completely detached from live ecosystems, utilizing mock layers.

​<b>Integration Test:</b> Validates combined interactions between systems—such as verifying your API router writes accurate structures directly to a real testing database instance.
</p>
</details>
​<details>
<summary><b>Q6: How do you check and maximize test coverage in Python?</b></summary>
<p>
Use the <code>coverage</code> tool or <code>pytest-cov</code> plugin. Running <code>pytest --cov=myapp</code> monitors executed statement tracks and produces code line maps indicating missing code test evaluations. It assists in ensuring edge cases inside error handling logic are appropriately exercised.
</p>
</details>
​<details>
<summary><b>Q7: What is Pytest Parameterization?</b></summary>
<p>
Instead of duplicating the same test function five times for different inputs, the <code>@pytest.mark.parametrize</code> decorator passes variable argument permutations directly into a single clean assertion block:
<pre><code>@pytest.mark.parametrize("input, expected", [(1, 2), (5, 6)])
def test_increment(input, expected):
assert input + 1 == expected
</code></pre>
</p>
</details>
​4. Git & Collaborative Workflows (Conflict Resolution at Scale)
​<details>
<summary><b>Q4: What is a detached HEAD state and how do you resolve it?</b></summary>
<p>
A detached HEAD happens when you check out a specific commit hash or remote tag directly rather than tracking a local development branch. Commits made here will not advance any branch. To keep updates safely, create a new feature branch tracking your current spot immediately using: <code>git checkout -b fix-branch-name</code>.
</p>
</details>
​<details>
<summary><b>Q5: What does <code>git stash pop</code> do compared to <code>git stash apply</code>?</b></summary>
<p>
​<code>git stash apply</code>: Restores shelved, uncommitted local changes from your active stash list but preserves the copy in the stash index.

​<code>git stash pop</code>: Restores the code changes to your workspace and automatically clears that specific entry out of your stash list completely.
</p>
</details>
​<details>
<summary><b>Q6: What is a fast-forward merge?</b></summary>
<p>
If the target branch history has not changed since you branched off, Git can simply move the pointer straight forward to the tip of your feature branch commit without creating a distinct merge commit node. If you want to force a visual merge commit history node, you run <code>git merge --no-ff</code>.
</p>
</details>
​5. CI/CD Pipelines (Enterprise GitHub Actions & Scaling)
​<details>
<summary><b>Q4: How do you use Matrix Strategies in GitHub Actions?</b></summary>
<p>
A matrix strategy lets you run your job across variations of your build configurations inside parallel runner environments. For instance, testing a Django app against Python versions 3.10, 3.11, and 3.12 concurrently with one configuration step setup.
<pre><code>strategy:
matrix:
python-version: [3.10, 3.11, 3.12]
</code></pre>
</p>
</details>  
​<details>
<summary><b>Q5: How do you secure pipeline secrets (DB credentials, cloud keys)?</b></summary>
<p>
Never hardcode tokens inside repository files. Instead, add them to your platform's encrypted repository settings (e.g., GitHub Settings -> Secrets and Variables -> Actions). Within the YAML configuration, fetch them securely using dynamic system reference variables like <code>${{ secrets.DATABASE_URL }}</code>.
</p>
</details>  
​<details>
<summary><b>Q6: How can you optimize and speed up lint/test workflow times?</b></summary>
<p>
​Implement <b>dependency caching</b> steps (caching <code>~/.cache/pip</code> or node modules based on lock file hashes).
  
​Run detached independent testing environments concurrently using matrix parallel configurations.

​Configure path-based filters so linter pipelines only trigger if code files actually change (e.g., ignoring <code>docs/*.md</code> updates).
</p>
</details>
​6. AI Knowledge (LLMs & Microservices)
​<details>
<summary><b>Q3: What are Embeddings and Vector Databases?</b></summary>
<p>
Embeddings translate natural text or unstructured queries into dense multidimensional arrays of numbers (vectors) representing semantic meaning. Vector Databases (like Pinecone, Milvus, or Chroma) index these arrays to perform extremely rapid mathematical cosine or Euclidean distance similarity checks. This is the foundation of semantic search in backend systems.
</p>
</details>
​<details>
<summary><b>Q4: How do you manage API rate limits or latency when integrating LLMs into a Django backend?</b></summary>
<p>
​Utilize <b>asynchronous task queues</b> (like Celery with Redis) so LLM API calls don't block the main web thread.

​Implement robust exponential-backoff retry logic (e.g., using the <code>tenacity</code> library) to handle token or rate limits.

​Cache repetitive or static prompt results using Redis to minimize computational overhead and costs.
</p>
</details>