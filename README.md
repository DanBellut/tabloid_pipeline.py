An automated Python project that collects real-time news about Germany from major media outlets and rewrites them into high-engagement, sensationalist tabloid-style summaries using OpenAI.

Instead of reading through dozens of different websites, this tool automatically pulls raw articles, focuses on highly debated domestic political topics, and outputs dramatic, punchy news reports directly into a database.

Features Multi-Source Aggregation: Automatically fetches real-time updates from top German news outlets (Tagesschau, WELT, Focus Online, FAZ, ZEIT Online).

AI Synthesis: Uses OpenAI (gpt-4o-mini) to merge overlapping stories from multiple outlets into a single, cohesive report.

Tabloid Journalistic Style: Applies punchy, short sentences and aggressive, capitalized trigger headlines to drive user engagement.

Emotional Angle: Specifically highlights public debates surrounding taxation, government performance, welfare, and cultural discussions to capture attention.

Database Storage: Saves processed articles, timestamps, and source links into a local SQLite database (automated_news.db).

Built for Scaling: Cleanly structured code, making it easy to add more countries (US, EU, China, India, Russia) in the future.

Tech Stack Language: Python 3.10+Parsing: feedparserAI Processing: OpenAI API (gpt-4o-mini)Database: SQLite3






























