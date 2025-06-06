import json
import os
import re

def sanitize_filename(name):
    """Converts name to lowercase hyphenated filename (e.g. 'ZEM Wellness Clinic Altea' -> 'zem-wellness-clinic-altea')"""
    return re.sub(r'[^a-z0-9\-]', '', name.lower().replace(" ", "-"))

def get_program_titles(clinic_filename_base):
    """Looks for JSON files in /programs/[clinic-name]/ and extracts 'Title' from each"""
    program_dir = os.path.join("programs", clinic_filename_base)
    program_titles = []

    if not os.path.isdir(program_dir):
        return program_titles  # Gracefully handle missing directory

    for file in os.listdir(program_dir):
        if file.endswith(".json"):
            file_path = os.path.join(program_dir, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    title = data.get("Title")
                    if title:
                        program_titles.append(title)
            except Exception as e:
                print(f"⚠️ Could not load program file: {file_path}. Reason: {e}")
                continue

    return program_titles

def generate_clinic_markdown(json_path, output_dir):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    name = data.get("Clinic name", "Unknown Clinic")
    filename = sanitize_filename(name)
    location = f"{data.get('Location (town)', '')}, {data.get('Location (country)', '')}"
    address = data.get("Location (address)", "")
    short_desc = data.get("Short description (less than 160 characters)", "")
    long_desc = data.get("Long description (500 characters)", "")
    sw_url = data.get("Serenity Ways URL", "")
    usp1 = f"**{data.get('USP 1 (title)', '')}:** {data.get('USP 1 (description in less than 160 characters)', '')}"
    usp2 = f"**{data.get('USP 2 (title)', '')}:** {data.get('USP 2 (description in less than 160 characters)', '')}"
    usp3 = f"**{data.get('USP 3 (title)', '')}:** {data.get('USP 3 (description in less than 160 characters)', '')}"
    approach = data.get("Health and wellness approach (less than 500 characters)", "")
    nutrition = data.get("Nutrition approach (less than 500 characters)", "")
    benefits = data.get("Exclusive benefits when booking with Serenity Ways", "")
    languages = data.get("Languages spoken", "")
    highlights = data.get("Location highlights", "")
    access = data.get("Access", "")
    family = data.get("Family friendly ?", "")
    pet = data.get("Pet friendly ?", "")
    booking_policy = data.get("Booking and payment policy", "")
    cancel_policy = data.get("Cancellation policy", "")

    faqs = []
    for i in range(1, 6):
        q = data.get(f"FAQ {i} - question")
        a = data.get(f"FAQ {i} - answer")
        if q and a:
            faqs.append((q, a))

    # Get related programs
    program_titles = get_program_titles(filename)
    if program_titles:
        programs_section = "## Programs at This Clinic\n\n" + "\n".join([f"- {title}" for title in program_titles]) + "\n\n"
    else:
        programs_section = ""

    # CTA
    cta = """
---

## Serenity Ways Insight

Looking for tailored guidance or exclusive benefits for your wellness journey?

Our Serenity Ways experts can help you choose the perfect retreat and unlock VIP advantages.

💬 [Whatsapp us for personalized advice](https://wa.me/33786553455?text=Can you help me with Serenity Ways?)
🛎️ Or [send your booking request](https://serenityways.com/pages/contact)
📧 Or email us at [concierge@serenityways.com](mailto:concierge@serenityways.com)

---

*This markdown was auto-generated to keep content accurate and up-to-date. For expert curation, trust Serenity Ways.*
"""

    # Combine all content
    md_content = f"""# {name}

**Location:** {location}
**Address:** {address}
**Languages Spoken:** {languages}

---

## Summary

{short_desc}

---

## Full Description

{long_desc}

---

## Unique Strengths

- {usp1}
- {usp2}
- {usp3}

---

## Health & Wellness Approach

{approach}

---

## Nutrition Approach

{nutrition}

---

## Serenity Ways Exclusive Benefits

{benefits}

[Explore on Serenity Ways]({sw_url})

---

## Practical Information

**Location Highlights:** {highlights}
**Access:** {access}
**Family Friendly:** {family}
**Pet Friendly:** {pet}

---

## Booking & Cancellation

**Booking Policy:** {booking_policy}
**Cancellation Policy:** {cancel_policy}

---

## FAQs

""" + "\n\n".join([f"**Q: {q}**\n\nA: {a}" for q, a in faqs]) + "\n\n" + programs_section + cta

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{filename}.md")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f"✅ Generated markdown: {output_path}")

# Example usage
if __name__ == "__main__":
    input_dir = "./clinics"
    output_dir = "./markdown/clinics"
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            input_path = os.path.join(input_dir, filename)
            generate_clinic_markdown(input_path, output_dir)
