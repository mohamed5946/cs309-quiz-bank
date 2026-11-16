#!/usr/bin/env python3
"""Build CS 309 quiz bank index.html from the H 201 template + cs309-quiz-data.json."""
import json, re, pathlib

work = pathlib.Path(__file__).parent
data = json.load(open(work / "cs309-quiz-data.json", encoding="utf-8"))
html = open(work / "index.html", encoding="utf-8").read()

# 1) Replace the embedded QUESTIONS array (single line starting with 'var QUESTIONS = [')
lines = html.split("\n")
for i, ln in enumerate(lines):
    if ln.strip().startswith("var QUESTIONS = ["):
        lines[i] = "      var QUESTIONS = " + json.dumps(data, ensure_ascii=False) + ";"
        break
else:
    raise SystemExit("QUESTIONS line not found")
html = "\n".join(lines)

# 2) Title + header
html = html.replace("<title>H 201 Quiz Bank</title>", "<title>CS 309 Quiz Bank</title>")
html = html.replace(
    '<h1>بنك أسئلة <span class="en">H 201</span></h1>',
    '<h1>بنك أسئلة <span class="en">CS 309</span></h1>',
)
html = html.replace(
    "ضبط وتوكيد الجودة — اختار إجابة أي سؤال، وهيظهرلك على طول تحت نفس السؤال إذا كانت صح ولا غلط، مع الإجابة النموذجية وشرح تفصيلي بالعربي بيحافظ على المصطلحات الإنجليزية زي ما هي. الدكتورة قالت الميدتيرم هييجي من الأسئلة دي.",
    "المعالجات الدقيقة ولغة التجميع (8086) — اختار إجابة أي سؤال، وهيظهرلك على طول تحت نفس السؤال إذا كانت صح ولا غلط، مع الإجابة النموذجية وشرح تفصيلي بالعربي بيحافظ على المصطلحات الإنجليزية زي ما هي. أسئلة للتدريب على الميدتيرم من التدريب والـ Assignments والسلايدز.",
)

# 3) Bank segmented control (5 banks) + allow wrapping on small screens
old_seg = '''<div class="seg" role="tablist" aria-label="اختيار البنك">
          <button data-bank="all" class="on">الكل (80)</button>
          <button data-bank="drill">التدريب (20)</button>
          <button data-bank="a1">Assignment 1 (30)</button>
          <button data-bank="a3">Assignment 3 (14)</button>
          <button data-bank="expected">أسئلة متوقعة (16)</button>
        </div>'''
new_seg = '''<div class="seg" role="tablist" aria-label="اختيار البنك">
          <button data-bank="all" class="on">الكل (110)</button>
          <button data-bank="drill">التدريب (20)</button>
          <button data-bank="a1">Assignment 1 (30)</button>
          <button data-bank="a3">Assignment 3 (14)</button>
          <button data-bank="expected">أسئلة متوقعة (16)</button>
          <button data-bank="past">الامتحان السابق (30)</button>
        </div>'''
assert old_seg in html, "seg block not found"
html = html.replace(old_seg, new_seg)
html = html.replace(
    '.seg{display:flex;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:4px;gap:4px;box-shadow:var(--shadow-sm)}',
    '.seg{display:flex;flex-wrap:wrap;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:4px;gap:4px;box-shadow:var(--shadow-sm)}',
)

# 4) Bank names used on the cards
old_names = 'var BANK_NAMES = { drill: "التدريب", a1: "Assignment 1", a3: "Assignment 3", expected: "أسئلة متوقعة" };'
new_names = 'var BANK_NAMES = { drill: "التدريب", a1: "Assignment 1", a3: "Assignment 3", expected: "أسئلة متوقعة", past: "الامتحان السابق" };'
assert old_names in html, "BANK_NAMES not found"
html = html.replace(old_names, new_names)

# 5) Footer
old_footer = "الأسئلة والإجابات من تدريب الميدتيرم (20 سؤال)، وحل Assignment 1 بخط الإيد، وأسئلة Assignment 3 المحلولة، وسلايدز شابتر 1 و 2 (د/ أشرف فهمي). الشروح مكتوبة بالعربي بشكل تفصيلي للتدريب مع الحفاظ على المصطلحات الإنجليزية زي ما هي.<br/>ملحوظة: حل Assignment 1 فيه غلطتين متصححين هنا — MOV CS, AX غلط (الـ CS مينفعش يتحمّل بـ MOV خالص)، و MOV AL, CH صح (الاتنين 8-bit).<br/>نتيجتك بتتحسب في الجلسة دي بس، ولو قفلت الصفحة وفتحتها هتبدأ من الأول."
new_footer = "الأسئلة والإجابات من تدريب الميدتيرم (20 سؤال)، وحل Assignment 1 بخط الإيد، وأسئلة Assignment 3 المحلولة، وسلايدز شابتر 1 و 2 (د/ أشرف فهمي)، وامتحان الميدتيرم التاني 2024/2025 (30 سؤال، 12-4-2025) — فلتر «الامتحان السابق». الشروح مكتوبة بالعربي بشكل تفصيلي للتدريب مع الحفاظ على المصطلحات الإنجليزية زي ما هي.<br/>ملحوظة: حل Assignment 1 فيه غلطتين متصححين هنا — MOV CS, AX غلط (الـ CS مينفعش يتحمّل بـ MOV خالص)، و MOV AL, CH صح (الاتنين 8-bit).<br/>نتيجتك بتتحسب في الجلسة دي بس، ولو قفلت الصفحة وفتحتها هتبدأ من الأول."
assert old_footer in html, "footer not found"
html = html.replace(old_footer, new_footer)

# 6) Safety: no 8088 anywhere
assert "8088" not in html, "8088 leaked into the page!"

open(work / "index.html", "w", encoding="utf-8").write(html)
print("built index.html:", len(html), "bytes;", len(data), "questions")
