# warm/project-b.md — Project B (Telegram-native CRM)

# Load when: Project B, bot @ProjectBBot, ProjectB.io, contact.project-b.com, Telegram-native CRM, business card scan.

## § Current pivot (Sep 1 2026)
- Keep as Telegram-first chat-style CRM (NOT Salesforce-clone).
- Differentiation pillars: (a) Telegram chat UX, (b) AI auto-enriches contact's company, (c) crypto payment rail.
- **Rejected:** hotel F&B AI direction, free-aggregator model, Salesforce-clone UI.

## § Live infra
- **Bot:** @ProjectBBot, deployed on Railway.
- **Web:** project-b.io (Cloudflare DNS, apex CNAME-flattened).
- **Supabase:** Pro plan. 7 tables + RLS.
- **Resend:** sender `ProjectB <hello@contact.project-b.com>` — subdomain verified.
- **FLASK_SECRET** SET on Railway.

## § Auth flow
- Web: bcrypt password (NOT Supabase Auth).
- Bot: /signup -> magic link -> ask password 2x (/skip opt-out).
- **Bot has NO delete_contact function** — system prompt redirects to project-b.io/dashboard.

## § Bot functionality
- AI system prompt: "plain text only, no markdown syntax".
- 6 M3 function-calling tools: list / find / add_contact / add_note / start_trip / stop_trip / update_contact.
- Schema: name, handle, company, title, email, phone, notes, source, search_vector, website.
- **AI must ASK for missing critical fields** (name, company) — never save partials.
- **Disambiguation rule:** search notes/company/title (vector includes all) not just name.
- **State must flow across turns** — explicit `focus_X` tool M3 calls.

## § Signup gate
- ALL real actions require signup: /list, /find, /trip, /send, AI chat, photo scan, contact share, /save.
- Only /start, /help, /signup, /stats stay open.
- **Better funding metric:** every bot interaction requires verified email.

## § Pricing
- Free=10 cards, Pro=$9.99/mo or $99/yr, Team=$49/mo.

## § Copy rules
- **Never mention Nick as founder.** Anonymous product/team framing.
- Max 2 mentions of chat app name in first 3 sections of landing page.
- Never mention LLM model name in landing copy.

## § Bug to remember
- Original system prompt leaked M3 model name + Supabase errors to users — replaced Jun 17.
- search_vector bug: needs to include all searchable fields, not just name.
