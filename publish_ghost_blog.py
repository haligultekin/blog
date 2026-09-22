"""Script to publish the eBay Lister blog post to Ghost CMS formatted in Kumuluzbad's style."""

import datetime
import sqlite3
import uuid

DB_PATH = "/home/ali/homelab-data/ghost/data/ghost.db"

title = "Automating the Vintage Archive: How We Built an AI-Powered eBay Lister for Heritage Denim"
slug = "automating-the-vintage-archive-ai-ebay-lister"
custom_excerpt = (
    "From single-stitch Levi's 501s to RRL selvedge, how Kumuluzbad built a containerized "
    "AI studio that auto-detects brand specs, extracts flat-lay measurements, and "
    "publishes directly to eBay via the REST API."
)
feature_image = "__GHOST_URL__/content/images/2026/09/ebay-vintage-denim-hero.jpg"

html_content = """
<figure class="kg-card kg-image-card"><img src="__GHOST_URL__/content/images/2026/09/ebay-vintage-denim-hero.jpg" class="kg-image" alt="Vintage Selvedge Analysis and eBay Listing Studio" loading="lazy"></figure><p>Reselling curated vintage denim — whether it's 1980s single-stitch <strong>Levi's 501s</strong>, <strong>Levi's Vintage Clothing (LVC)</strong> reproductions, <strong>RRL (Double RL)</strong> selvedge truckers, or 21oz <strong>Iron Heart</strong> heavyweights — is an exercise in precision. Every piece requires keyword frontloading for search ranking, flat-lay measurement tables, and exact API payload formatting.</p><p>Kumuluzbad's rule: <em>'A dwarf of the station and the atelier knows that if a task takes 15 minutes of manual clicking for every single pair of jeans, it's not a workflow — it's an obstacle. We forge tools so the maker can stay at the bench.'</em></p><p>To eliminate manual data entry and streamline the vintage archive reselling workflow, we built and deployed a custom, containerized web application: <strong>eBay Resell Studio</strong>.</p><h2 id="the-architecture-docker-python-and-ebay-rest-api">The Architecture: Docker, Python &amp; eBay REST API</h2><p>The application is built using Python 3.13 and Flask, containerized under Docker Compose as <code>ebay-lister</code>, listening on port <code>5050</code> alongside our homelab stack (Immich, Plex, Homepage, Ghost).</p><p>Here is how the end-to-end publishing pipeline operates:</p><ol><li><strong>Image Ingestion &amp; Web Compression:</strong> Users upload high-resolution smartphone photos. Pillow automatically corrects EXIF rotation, scales images to 1600x1600 px (eBay's recommended resolution), and compresses them to 85% quality JPEGs — slashing upload sizes by 85%.</li><li><strong>Brand &amp; Size Dropdown Selection:</strong> Dedicated selector dropdowns support top heritage labels (Levi's, RRL, LVC, Iron Heart, Lee, Wrangler, Carhartt, etc.) and dual size systems (Jeans waist sizes W28–W44 and alpha sizes XXS–3XL).</li><li><strong>AI Title &amp; Keyword SEO Engine:</strong> Analyzes photos and keyword notes to craft high-converting eBay titles strictly under the 80-character limit (e.g. <code>VINTAGE Levis 501 Big E Redline Selvedge Jeans Made in USA W32 L34</code>).</li><li><strong>1-Click eBay API Publishing:</strong> Executes the modern 3-stage eBay RESTful Inventory API flow.</li></ol><h2 id="under-the-hood-the-ebay-inventory-api-workflow">Under the Hood: The eBay Inventory API Workflow</h2><p>Unlike legacy SOAP/XML Trading APIs, the modern eBay Inventory API v1 relies on a clean RESTful sequence:</p><pre><code>1. OAuth 2.0 Token Acquisition:
   POST https://api.ebay.com/identity/v1/oauth2/token (Cached for 2 hours)

2. Create/Update Inventory Item:
   PUT https://api.ebay.com/sell/inventory/v1/inventory_item/{sku}
   Payload: Title (&lt;=80 chars), HTML description, image URLs, aspects dict.

3. Create Merchant Offer:
   POST https://api.ebay.com/sell/inventory/v1/offer
   Payload: SKU, category ID (11483 for Jeans), price, seller policies.

4. Publish Offer to eBay:
   POST https://api.ebay.com/sell/inventory/v1/offer/{offerId}/publish
   Returns: Live eBay Listing ID
</code></pre><h2 id="automating-flat-lay-measurements-and-condition-reports">Automating Flat-Lay Measurements &amp; Condition Reports</h2><p>Vintage buyers on eBay make purchase decisions based on actual measured dimensions rather than tagged sizes. The studio automatically formats standardized HTML measurement tables for every item:</p><ul><li><strong>Tagged Size vs. Measured Waist</strong> (across waist x 2)</li><li><strong>Inseam Length</strong></li><li><strong>Front Rise &amp; Leg Opening</strong></li><li><strong>Authenticity &amp; Fade Patina Breakdown</strong></li></ul><h2 id="deployment-and-homelab-integration">Deployment &amp; Homelab Integration</h2><p>The studio runs 24/7 inside our homelab ecosystem, accessible on the local network at <code>http://192.168.1.10:5050</code> with persistence mounted at <code>/home/ali/homelab-data/ebay_lister/uploads</code>.</p><p>By bringing AI-assisted copywriting, web-compressed image pipelines, and direct API publishing together, listing vintage denim has shifted from a 15-minute tedious process to a 30-second tap on a smartphone.</p>
""".strip()

plaintext_content = (
    "Reselling curated vintage denim—whether it's 1980s single-stitch Levi's 501s, "
    "LVC, RRL, or Iron Heart—is an exercise in precision. Kumuluzbad built an AI-powered "
    "eBay Lister Web Studio containerized under Docker Compose on port 5050."
)

now_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
post_id = uuid.uuid4().hex[:24]
post_uuid = str(uuid.uuid4())
published_by = "6a1df6850867fa00018b311f"  # Kumuluzbad ID

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT id FROM posts WHERE slug = ?", (slug,))
    existing = cur.fetchone()

    if existing:
        print(f"[*] Updating existing post '{slug}' in Kumuluzbad style...")
        cur.execute(
            """
            UPDATE posts SET
                title = ?,
                custom_excerpt = ?,
                feature_image = ?,
                html = ?,
                plaintext = ?,
                updated_at = ?
            WHERE slug = ?
            """,
            (title, custom_excerpt, feature_image, html_content, plaintext_content, now_str, slug),
        )
    else:
        print(f"[*] Inserting new blog post '{title}' into Ghost database...")
        cur.execute(
            """
            INSERT INTO posts (
                id, uuid, title, slug, html, plaintext, feature_image, featured,
                type, status, locale, visibility, email_recipient_filter, comment_id,
                created_at, updated_at, published_at, published_by, custom_excerpt,
                show_title_and_feature_image
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                post_id,
                post_uuid,
                title,
                slug,
                html_content,
                plaintext_content,
                feature_image,
                0,
                "post",
                "published",
                "en",
                "public",
                "all",
                post_id,
                now_str,
                now_str,
                now_str,
                published_by,
                custom_excerpt,
                1,
            ),
        )

    conn.commit()
    conn.close()
    print("[SUCCESS] Blog post updated successfully in Kumuluzbad voice & Ghost format!")

if __name__ == "__main__":
    main()
