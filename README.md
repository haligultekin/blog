# Ghost Blog Auto-Publisher

A Python automation script designed to interface with the Ghost CMS API. This script allows you to easily draft and publish blog posts programmatically, making it perfect for automated content pipelines, reseller studios, and AI agents.

## 🚀 Features
* **Automated Publishing:** Push formatted HTML content directly to your Ghost blog.
* **Tagging & Metadata:** Automatically assign tags, authors, and SEO metadata.
* **Headless Integration:** Perfect for integrating with background jobs, Telegram bots, or AI content agents.

## 🛠 Usage
Make sure you have your Ghost Admin API Key configured.

```python
from publish_ghost_blog import GhostPublisher

# Example usage
publisher = GhostPublisher(
    api_url="https://your-blog.ghost.io",
    admin_api_key="YOUR_ADMIN_API_KEY"
)

publisher.publish(
    title="My Awesome Post",
    html="<p>This is the content</p>",
    tags=["Automation", "Python"]
)
```

## 📝 Inspiration
This script was extracted from a real-world vintage reseller pipeline to help others automate their own Ghost blogs and content distribution. Feel free to fork and modify!
