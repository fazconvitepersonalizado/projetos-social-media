# Meta Graph API — Instagram Publishing
> API version: **v25.0** | Updated: May 2026

## Required credentials

| Variable | Where to get |
|---|---|
| `INSTAGRAM_ACCOUNT_ID` | Meta Business Suite → Settings → Instagram Accounts → Account ID |
| `INSTAGRAM_ACCESS_TOKEN` | Meta for Developers → Graph API Explorer → generate token with required permissions |

Store both in `.env` at the project root. Never commit this file.

---

## Authentication flows

### Instagram Login (Business Login for Instagram)

| Field | Value |
|---|---|
| Host | `graph.instagram.com` |
| Token | Instagram User Access Token |

**Required permissions:**
- `instagram_business_basic`
- `instagram_business_content_publish`

---

### Facebook Login (Facebook Login for Business)

| Field | Value |
|---|---|
| Host | `graph.facebook.com` |
| Video upload host | `rupload.facebook.com` |
| Token | Facebook Page Access Token |

**Required permissions:**
- `instagram_basic`
- `instagram_content_publish`
- `pages_read_engagement`

**Additional permissions (when needed):**
- `ads_management` + `ads_read` — if user has a role via Business Manager
- `catalog_management` + `instagram_shopping_tag_products` — for product tags
- `instagram_branded_content_creator` or `instagram_basic` — for Partnership Ads Label
- `instagram_manage_engagement` — to like/unlike via API *(new Apr/2026)*
- `instagram_manage_contents` — to delete media via API *(new Dec/2025)*

> Deprecated parameters (Jun/2025): `enable_fb_login` and `force_authentication` in Business Login.

---

## Publishing flow

```
[Auth] → [1. Create Container] → [2. Upload video*] → [3. Publish]
```

Step 2 is only required for videos using Resumable Upload Session.

---

## Step 1 — Create Container

**Endpoint:** `POST /<IG_ID>/media`

Containers expire in **24 hours**. Limit: **400 containers per account per 24h**.

### Image

```bash
curl -X POST "https://graph.instagram.com/v25.0/<IG_ID>/media" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d "image_url=https://example.com/photo.jpg" \
  -d "caption=My post #hashtag @user" \
  -d "alt_text=Alternative description" \
  -d "location_id=<PAGE_ID>"
```

| Parameter | Required | Type | Description |
|---|---|---|---|
| `image_url` | ✅ | string | Public JPEG URL |
| `caption` | ❌ | string | Max 2200 chars, 30 hashtags, 20 @ tags |
| `alt_text` | ❌ | string | Accessibility text, max 1000 chars. Not supported in Reels/Stories. *(new Mar/2025)* |
| `location_id` | ❌ | string | Location Page ID |
| `user_tags` | ❌ | array | `[{"username":"user","x":0.5,"y":0.5}]` |
| `product_tags` | ❌ | array | Product tags (requires extra permissions) |
| `is_carousel_item` | ❌ | boolean | `true` if item is part of a carousel |
| `is_paid_partnership` | ❌ | boolean | Activates "Paid partnership" label *(new Apr/2026)* |
| `branded_content_sponsor_ids` | ❌ | array | IDs of up to 2 partner brands *(new Apr/2026)* |

---

### Reel / Video

```bash
curl -X POST "https://graph.instagram.com/v25.0/<IG_ID>/media" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d "media_type=REELS" \
  -d "video_url=https://example.com/video.mp4" \
  -d "caption=My reel" \
  -d "share_to_feed=true" \
  -d "cover_url=https://example.com/thumb.jpg" \
  -d "collaborators=user1,user2"
```

| Parameter | Required | Type | Description |
|---|---|---|---|
| `media_type` | ✅ | string | `REELS` or `VIDEO` |
| `video_url` | ✅* | string | Public video URL (MOV or MP4) |
| `upload_type` | ✅* | string | `resumable` — alternative to `video_url` for large files |
| `caption` | ❌ | string | Reel caption |
| `share_to_feed` | ❌ | boolean | Also share to main feed |
| `cover_url` | ❌ | string | Cover image URL (JPEG, 9:16 ratio) |
| `thumb_offset` | ❌ | integer | Offset in ms for auto-generated thumbnail |
| `audio_name` | ❌ | string | Original audio name. Can only be renamed once |
| `collaborators` | ❌ | array | Up to 3 usernames as collaborators |
| `user_tags` | ❌ | array | User tags in video |
| `location_id` | ❌ | string | Location Page ID |
| `trial_params` | ❌ | object | Trial Reel configuration *(new Dec/2025)* |
| `is_paid_partnership` | ❌ | boolean | Paid partnership label *(new Apr/2026)* |
| `branded_content_sponsor_ids` | ❌ | array | Partner brand IDs *(new Apr/2026)* |

> Use `video_url` OR `upload_type=resumable`, never both. Reels cannot appear in carousels.

---

### Carousel

**Step A — Create each item container:**

```bash
# Image item
curl -X POST "https://graph.instagram.com/v25.0/<IG_ID>/media" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d "image_url=https://example.com/img1.jpg" \
  -d "is_carousel_item=true"

# Video item (resumable)
curl -X POST "https://graph.instagram.com/v25.0/<IG_ID>/media" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d "media_type=VIDEO" \
  -d "is_carousel_item=true" \
  -d "upload_type=resumable"
```

**Step B — Create the carousel container:**

```bash
curl -X POST "https://graph.instagram.com/v25.0/<IG_ID>/media" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d "media_type=CAROUSEL" \
  -d "caption=My carousel" \
  -d "children=<ID_1>,<ID_2>,<ID_3>" \
  -d "collaborators=user1"
```

| Parameter | Required | Type | Description |
|---|---|---|---|
| `media_type` | ✅ | string | Must be `CAROUSEL` |
| `children` | ✅ | string | Container IDs separated by commas. Max 10 |
| `caption` | ❌ | string | Carousel caption |
| `collaborators` | ❌ | array | Up to 3 collaborators (usernames) |
| `location_id` | ❌ | string | Location |
| `product_tags` | ❌ | array | Product tags |

**Limitations:**
- Maximum 10 items (images, videos, or mix)
- Images cropped based on first item's ratio (default 1:1)
- Reels not supported as carousel items

---

### Story

```bash
# Image story
curl -X POST "https://graph.instagram.com/v25.0/<IG_ID>/media" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d "image_url=https://example.com/story.jpg" \
  -d "media_type=STORIES" \
  -d 'user_tags=[{"username":"user","x":0.5,"y":0.3}]'

# Video story
curl -X POST "https://graph.instagram.com/v25.0/<IG_ID>/media" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d "video_url=https://example.com/story.mp4" \
  -d "media_type=STORIES"
```

| Parameter | Required | Type | Description |
|---|---|---|---|
| `media_type` | ✅ | string | Must be `STORIES` |
| `image_url` | ✅* | string | Image URL (for image stories) |
| `video_url` | ✅* | string | Video URL (for video stories) |
| `user_tags` | ❌ | array | User mentions with x,y coordinates *(expanded Jul/2025)* |

**Limitations:**
- Stories expire in 24 hours
- Stickers (link, poll, location) not supported via API
- When querying `media_type` on a published story, the value returned is `IMAGE` or `VIDEO` — use `media_product_type` to confirm it's a story

---

## Step 2 — Video Upload (Resumable)

Only needed when `upload_type=resumable` was used. Upload goes to `rupload.facebook.com`.

**Upload from local file:**

```bash
curl -X POST "https://rupload.facebook.com/ig-api-upload/v25.0/<IG_CONTAINER_ID>" \
  -H "Authorization: OAuth <ACCESS_TOKEN>" \
  -H "offset: 0" \
  -H "file_size: <SIZE_IN_BYTES>" \
  --data-binary "@my_video.mp4"
```

**Upload from hosted URL:**

```bash
curl -X POST "https://rupload.facebook.com/ig-api-upload/v25.0/<IG_CONTAINER_ID>" \
  -H "Authorization: OAuth <ACCESS_TOKEN>" \
  -H "file_url: https://example.com/video.mp4"
```

**Success response:**
```json
{ "success": true, "message": "Upload successful." }
```

---

## Step 3 — Publish Container

**Endpoint:** `POST /<IG_ID>/media_publish`

```bash
curl -X POST "https://graph.instagram.com/v25.0/<IG_ID>/media_publish" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d "creation_id=<IG_CONTAINER_ID>"
```

**Success response:**
```json
{ "id": "<IG_MEDIA_ID>" }
```

Same endpoint works for single and carousel containers.

---

## Container status polling

Check before publishing or when `media_publish` doesn't return the ID:

```
GET /<IG_CONTAINER_ID>?fields=status_code
```

| Status | Meaning |
|---|---|
| `FINISHED` | Ready to publish via `/media_publish` |
| `IN_PROGRESS` | Still processing — wait |
| `PUBLISHED` | Already published successfully |
| `ERROR` | Publishing process failed |
| `EXPIRED` | Container not published within 24h — create a new one |

> Recommended: check once per minute, for up to 5 minutes.

---

## Trial Reels

Trial Reels are visible only to non-followers. Include `trial_params` when creating the container:

```bash
curl -X POST "https://graph.instagram.com/v25.0/<IG_ID>/media" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d "media_type=REELS" \
  -d "video_url=https://example.com/video.mp4" \
  -d 'trial_params={"graduation_strategy":"MANUAL"}'
```

| `graduation_strategy` | Description |
|---|---|
| `MANUAL` | Trial Reel can be graduated manually in the app |
| `SS_PERFORMANCE` | Automatically graduated if it performs well |

*(Available via API since Dec/2025)*

---

## Partnership Ads Label

Adds "Paid partnership" label at publish time, without manual action in the app.

```bash
curl -X POST "https://graph.facebook.com/v25.0/<IG_USER_ID>/media" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d "image_url=<IMAGE_URL>" \
  -d "caption=<CAPTION>" \
  -d "is_paid_partnership=true" \
  -d "branded_content_sponsor_ids=[<BRAND_ID_1>,<BRAND_ID_2>]"
```

- Max 2 sponsors per post
- Sponsored accounts must be professional accounts
- Not supported on close friends posts or remixed media

---

## Media specs

### Image (feed)

| Spec | Value |
|---|---|
| Format | JPEG only (MPO and JPS not supported) |
| Max size | 8 MB |
| Aspect ratio | 4:5 to 1.91:1 |
| Min width | 320px (auto-scaled) |
| Max width | 1440px (auto-reduced) |
| Color space | sRGB (others auto-converted) |

### Reel

| Spec | Value |
|---|---|
| Container | MOV or MP4 (MPEG-4 Part 14, no edit lists, moov atom at start) |
| Duration | 3 seconds – 15 minutes |
| Max size | 300 MB |
| Recommended ratio | 9:16 |
| Max width | 1920px |
| Frame rate | 23–60 FPS |
| Video codec | H264 or HEVC, progressive, closed GOP, 4:2:0 |
| Video bitrate | VBR, max 25Mbps |
| Audio codec | AAC, max 48kHz, mono or stereo |
| Audio bitrate | 128kbps |

### Story — Image

| Spec | Value |
|---|---|
| Format | JPEG |
| Max size | 8 MB |
| Recommended ratio | 9:16 |
| Color space | sRGB |

### Story — Video

| Spec | Value |
|---|---|
| Container | MOV or MP4 |
| Duration | 3 seconds – 60 seconds |
| Max size | 100 MB |
| Recommended ratio | 9:16 |
| Frame rate | 23–60 FPS |
| Video codec | H264 or HEVC, progressive, closed GOP, 4:2:0 |
| Video bitrate | VBR, max 25Mbps |
| Audio codec | AAC, max 48kHz |

---

## Rate limits

| Limit | Value |
|---|---|
| Posts via API per account | 100 / 24h (rolling window) |
| Carousels per account | 50 / 24h |
| Containers created per account | 400 / 24h |
| Comment reply calls | 750 / hour per account |

Carousels count as 1 post toward the general limit. Limit applied at `/media_publish`.

**Check current usage:**

```
GET /<IG_ID>/content_publishing_limit
```

---

## New endpoints (2025–2026)

### Delete media *(Dec/2025)*

Removes posts, carousels, Reels and Stories.

```
DELETE /{ig_media_id}
```

Requires `instagram_manage_contents` permission.

---

### Collaboration Invites API *(Dec/2025)*

Accept or decline collaboration invites on posts.

```
GET  /<IG_USER_ID>/collaboration_invites
POST /<IG_USER_ID>/collaboration_invites
```

Requires `instagram_basic` permission.

---

### Collaborative Media API *(Apr/2026)*

Fetch all media where the user is an accepted collaborator.

```
GET /<IG_USER_ID>/collaborative_media
GET /<IG_USER_ID>?fields=collaborative_media_search.media_id(<IG_MEDIA_ID>)
```

---

### Like / Unlike API *(Apr/2026)*

Like and unlike posts, Reels and comments on behalf of the user.

```
POST   /<IG_USER_ID>/likes   ?media_id=<ID>  or  ?comment_id=<ID>
DELETE /<IG_USER_ID>/likes   ?media_id=<ID>  or  ?comment_id=<ID>
```

Requires `instagram_manage_engagement`. Stories and private accounts not supported.

---

### New engagement fields on IG Media *(Apr/2026)*

```
GET /{ig_media_id}?fields=reposts_count,saved_count,shares_count
```

---

### Aggregate cross-platform metrics *(Apr/2026)*

Combined totals from Instagram + Facebook + boosted media:

```
GET /{ig_media_id}?fields=total_like_count,total_comments_count,total_views_count
GET /{ig_media_id}/insights?metric=total_likes,total_comments,total_views
```

---

### New Insights metrics *(Dec/2025)*

**Media:** `reels_skip_rate`, `reposts`, `crossposted_views`, `facebook_views`

**User:** `reposts`

---

## catbox.moe upload (anonymous hosting)

```python
import requests

def upload_to_catbox(file_path: str) -> str:
    with open(file_path, "rb") as f:
        r = requests.post(
            "https://catbox.moe/user/api.php",
            data={"reqtype": "fileupload", "userhash": ""},
            files={"fileToUpload": f},
        )
    r.raise_for_status()
    return r.text.strip()  # returns direct URL, e.g. https://files.catbox.moe/abc123.png
```

Files persist indefinitely once uploaded. No rate limit for anonymous uploads.

---

## Common errors

| Code / Status | Cause | Fix |
|---|---|---|
| 190 | Token expired or invalid | Refresh token at Meta for Developers |
| 10 | Permission missing | Re-generate token with required permissions |
| 9007 | Account not Business/Creator | Convert account in Instagram settings |
| 2207026 | Image URL not publicly accessible | Re-upload to catbox.moe |
| 2207006 | Too many slides (max 10) | Reduce to ≤10 slides |
| Container `EXPIRED` | Not published within 24h | Create new container |
| Container `ERROR` | Invalid or inaccessible media | Check URL and media specs |
| `INSTAGRAM_PLATFORM_API__PERMISSION` | Missing permission | Check token and app permissions |
| Rate limit hit | Over 100 posts/24h | Wait for window reset or reduce frequency |
