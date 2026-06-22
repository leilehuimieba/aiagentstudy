# DuckDB Quack: Client/Server Protocol over HTTP for Multi-User Analytics

- BestBlogs URL: https://www.bestblogs.dev/article/66368033
- Original publisher URL: https://www.infoq.com/news/2026/05/duckdb-quack-protocol/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global
- Source: BestBlogs / InfoQ
- Publish time: 2026-05-31 19:17:00
- Capture route: article discovered from logged-in Chrome/OpenCLI profile `qmvqcrb8` latest article feed page 3; page/content captured from BestBlogs resource APIs
- Extracted chars: 4490

---

DuckDB has recently announced Quack, a new remote protocol over HTTP that lets multiple DuckDB instances connect to and work with the same database over a network. The protocol introduces client-server capabilities to a database that was previously mostly local and embedded.

   Keeping DuckDB’s lightweight workflow and SQL compatibility, Quack makes it easier to share datasets, support concurrent users, run analytics remotely, and build production-style data services without switching to a heavier, more traditional database system. Compared to existing approaches, Quack is designed to be simpler to use and significantly faster.

   

   Source: DuckDB blog

   Quack allows multiple applications to access the same DuckDB database simultaneously over standard HTTP connections, using DuckDB’s native data format. DuckDB says this approach can move large datasets about 3.5× faster than Arrow Flight and significantly faster than PostgreSQL.

   Released under the permissive MIT License, DuckDB is a popular open source analytical database designed for fast SQL queries on large datasets, directly from local files, applications, or notebooks. Like SQLite, it is an in-process database that can be embedded within an application without requiring a separate database server. Introducing Quack, the team writes:

   
    With Quack, DuckDB can now be useful in a wide range of new use cases, where centralizing state is more important than hyper-local querying. We have already had to learn that data is not always local with the rise of data lakes. Speaking of lakes, Quack is also going to be integrated into DuckLake so that DuckDB itself can be a remotely-accessible Catalog server.

   

   DuckDB decided not to use Arrow Flight SQL, a protocol for interacting with SQL databases using the Arrow in-memory format and the Flight RPC framework, because they wanted full control over how data is transferred and how the protocol evolves. They also claim that Quack is more efficient for small queries as it can send a query and return results in a single network round trip. The team adds:

   
    We feel that in order to be able to keep innovating in data systems, we cannot allow ourselves to be restricted by formats that are controlled externally.

   

   The Hacker News response was largely positive, with developers viewing it as an important step toward shared, multi-user analytics workflows while keeping DuckDB lightweight and easy to deploy. Ryan Glover, managing principal at Lattice Engineering, comments:

   
    This is rad. I've been eyeballing using DuckDB in my firm's internal app framework and this just solved the "but how do I horizontally scale this" problem. Kudos to the DuckDB folks. Love "Quack" for the protocol name, too.

   

   User kvlonge adds on Reddit:

   
    Being able to spin up DuckDB on a server and have people talk to it remotely like a 'normal' DB will be such a big unlock.

   

   DuckDB plans to integrate Quack with DuckLake, improve performance, and ship a production-ready release with DuckDB 2.0 later in 2026. The team is also working on better support for remote databases, higher transaction throughput, customizable protocol extensions, and replication features.

   In the "From DeepSeek to Quack: When the Dream of Distributed DuckDB Started to Feel Real" article, Amir Sefati highlights the advantage of DuckDB instances talking to each other:

   
    When you combine that with object storage, DuckLake, Parquet, and vector databases, you get a very pragmatic architecture for modern AI and data engineering. Not because it is trendy. Because it removes unnecessary complexity.

   

   Discussing further use cases, such as a browser tab talking directly to a DuckDB server or notebook-to-notebook query forwarding, Mehdi Ouazza, data engineer and developer advocate at MotherDuck, a cloud data warehouse built on the open-source DuckDB query engine, concludes:

   
    Can we finally retire the "DuckDB has no multi-writer support" take? There are plenty of options out there now, just depends how you want to slice and dice.

   

   Support for the new protocol currently requires the Quack extension in both DuckDB instances. The recently released DuckDB v1.5.3 supports Quack as an autoloadable core extension and as a DuckLake catalog.

   Hannes Mühleisen, creator of the DuckDB database and CEO of DuckDB Labs, previously presented a QCon session on in-process analytical data management with DuckDB.
